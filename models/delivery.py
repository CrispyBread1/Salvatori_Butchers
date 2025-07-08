class Delivery:
    def __init__(self, created_at, product, quantity, receipt_image, notes, id, vehicle_temperature, driver_name, license_plate, created_by, batch_code, origin, product_temperature, kill_date, use_by, red_tractor, rspca, slaughter_number, cut_number, organic_assured, supplier, date):
        self.id = id
        self.created_at = created_at
        self.product = product
        self.receipt_image = receipt_image
        self.quantity = quantity
        self.notes = notes
        self.vehicle_temperature = vehicle_temperature
        self.product_temperature = product_temperature
        self.driver_name = driver_name
        self.created_by = created_by
        self.license_plate = license_plate
        self.batch_code = batch_code
        self.origin = origin
        self.kill_date = kill_date
        self.use_by = use_by
        self.slaughter_number = slaughter_number
        self.cut_number = cut_number
        self.red_tractor = red_tractor
        self.rspca = rspca
        self.organic_assured = organic_assured
        self.supplier = supplier
        self.date = date

  # created_at timestamp with time zone not null default now(),
  # product integer null,
  # quantity integer null,
  # receipt_image text null,
  # notes text null,
  # id uuid not null default gen_random_uuid (),
  # vehicle_temperature text null,
  # driver_name text null,
  # license_plate text null,
  # created_by uuid null,
  # batch_code integer null,
  # origin text null,
  # product_temperature text null,
  # kill_date timestamp with time zone null,
  # use_by timestamp with time zone null,
  # red_tractor boolean null,
  # rspca boolean null,
  # slaughter_number text null,
  # cut_number text null,
  # organic_assured boolean null,
  # supplier text null,
  # date text null,

