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


      const action = body.action || "todays"

      let payload


      if (action === "todays") {

          if (!body.date) {

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


          payload = [
              {
                  field: "INVOICE_DATE",
                  type: "eq",
                  value: body.date
              }
          ]

      } else if (action === "todays_new") {

          if (!body.date || !body.previous_fetch) {

              return Response.json(
                  {
                      success: false,
                      message: "Date and previous fetch are required."
                  },
                  {
                      status: 400
                  }
              )
          }


          payload = [
              {
                  field: "INVOICE_DATE",
                  type: "eq",
                  value: body.date
              },
              {
                  field: "RECORD_CREATE_DATE",
                  type: "gt",
                  value: body.previous_fetch
              }
          ]

      } else if (action === "customer_month") {

          if (
              !body.customer_code ||
              !body.start_month ||
              !body.end_month
          ) {

              return Response.json(
                  {
                      success: false,
                      message:
                          "Customer code, start month and end month " +
                          "are required."
                  },
                  {
                      status: 400
                  }
              )
          }


          payload = [
              {
                  field: "ACCOUNT_REF",
                  type: "eq",
                  value: body.customer_code
              },
              {
                  field: "INVOICE_DATE",
                  type: "gte",
                  value: body.start_month
              },
              {
                  field: "INVOICE_DATE",
                  type: "lt",
                  value: body.end_month
              }
          ]

      } else if (action === "refresh") {

          if (!body.date || !body.original_fetch) {

              return Response.json(
                  {
                      success: false,
                      message: "Date and original fetch are required."
                  },
                  {
                      status: 400
                  }
              )
          }


          if (body.previous_fetch) {

              payload = [
                  {
                      field: "INVOICE_DATE",
                      type: "eq",
                      value: body.date
                  },
                  {
                      field: "RECORD_CREATE_DATE",
                      type: "lte",
                      value: body.original_fetch
                  },
                  {
                      field: "RECORD_CREATE_DATE",
                      type: "gte",
                      value: body.previous_fetch
                  }
              ]

          } else {

              payload = [
                  {
                      field: "INVOICE_DATE",
                      type: "eq",
                      value: body.date
                  },
                  {
                      field: "RECORD_CREATE_DATE",
                      type: "lte",
                      value: body.original_fetch
                  }
              ]
          }

      } else if (action === "last_week") {

          if (!body.date || !body.date_week_ago) {

              return Response.json(
                  {
                      success: false,
                      message:
                          "Date and previous date are required."
                  },
                  {
                      status: 400
                  }
              )
          }


          payload = [
              {
                  field: "INVOICE_DATE",
                  type: "lte",
                  value: body.date
              },
              {
                  field: "INVOICE_DATE",
                  type: "gte",
                  value: body.date_week_ago
              }
          ]

      } else {

          return Response.json(
              {
                  success: false,
                  message: "Unknown Sage invoice action."
              },
              {
                  status: 400
              }
          )
      }


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
                  `Sage invoice request failed for ${action}: ` +
                  `HTTP ${sageResponse.status}`
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


          console.log(
              `Sage invoice action ${action}: ` +
              `${sageData?.results?.length ?? 0} invoices`
          )


          return Response.json(
              sageData,
              {
                  status: 200
              }
          )

      } catch (error) {

          console.error(
              `Unable to complete Sage invoice action ${action}:`,
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
