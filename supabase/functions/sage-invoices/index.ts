export default {

  fetch: async (req: Request) => {

      if (req.method !== "POST") {

          return Response.json(
              {
                  success: false,
                  message: "Method not allowed."
              },
              {
                  status: 405
              }
          )
      }


      const supabaseUrl = Deno.env.get("SUPABASE_URL")

      const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY")

      const sageApiUrl = Deno.env.get("SAGE_API_URL")

      const sageApiToken = Deno.env.get("SAGE_API_TOKEN")


      if (!supabaseUrl || !supabaseAnonKey) {

          console.error(
              "Supabase authentication configuration is missing."
          )

          return Response.json(
              {
                  success: false,
                  message: "Authentication configuration is unavailable."
              },
              {
                  status: 500
              }
          )
      }


      if (!sageApiUrl || !sageApiToken) {

          console.error(
              "Sage environment variables are missing."
          )

          return Response.json(
              {
                  success: false,
                  message: "Sage configuration is unavailable."
              },
              {
                  status: 500
              }
          )
      }


      const authorization = req.headers.get("Authorization")


      if (!authorization) {

          return Response.json(
              {
                  success: false,
                  message: "Authorization is required."
              },
              {
                  status: 401
              }
          )
      }


      try {

          const authResponse = await fetch(
              `${supabaseUrl}/auth/v1/user`,
              {
                  method: "GET",
                  headers: {
                      "apikey": supabaseAnonKey,
                      "Authorization": authorization
                  }
              }
          )


          if (!authResponse.ok) {

              console.error(
                  `Supabase authentication failed: ` +
                  `HTTP ${authResponse.status}`
              )

              return Response.json(
                  {
                      success: false,
                      message: "Invalid or expired session."
                  },
                  {
                      status: 401
                  }
              )
          }

      } catch (error) {

          console.error(
              "Unable to verify Supabase user:",
              error
          )

          return Response.json(
              {
                  success: false,
                  message: "Unable to verify user."
              },
              {
                  status: 500
              }
          )
      }


      let body

      try {

          body = await req.json()

      } catch {

          return Response.json(
              {
                  success: false,
                  message: "Invalid request body."
              },
              {
                  status: 400
              }
          )
      }


      const date = body.date


      if (!date) {

          return Response.json(
              {
                  success: false,
                  message: "Date is required."
              },
              {
                  status: 400
              }
          )
      }


      const payload = [
          {
              field: "INVOICE_DATE",
              type: "eq",
              value: date
          }
      ]


      try {

          const sageResponse = await fetch(
              `${sageApiUrl.replace(/\/$/, "")}/api/searchInvoice`,
              {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                      "AuthToken": sageApiToken
                  },
                  body: JSON.stringify(payload)
              }
          )


          if (!sageResponse.ok) {

              console.error(
                  `Sage request failed: HTTP ${sageResponse.status}`
              )

              return Response.json(
                  {
                      success: false,
                      message: "Sage request failed."
                  },
                  {
                      status: 502
                  }
              )
          }


          const sageData = await sageResponse.json()


          return Response.json(
              sageData,
              {
                  status: 200
              }
          )

      } catch (error) {

          console.error(
              "Unable to connect to Sage:",
              error
          )

          return Response.json(
              {
                  success: false,
                  message: "Unable to connect to Sage."
              },
              {
                  status: 502
              }
          )
      }
  }
}
