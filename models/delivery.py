class Delivery:
    def __init__(self, id, created_at, product, receipt_image, quantity, notes, vehicle_temperature, product_temperature, driver_name, license_plate, created_by, batch_code, origin, product_temp, kill_date, use_by, slaughter_number, cut_number, red_tractor, rspca, organic_assured, supplier):
        self.id = id
        self.created_at = created_at
        self.product = product
        self.receipt_image = receipt_image
        self.quantity = quantity
        self.notes = notes
        self.vehicle_temperature = vehicle_temperature
        self.product_temperature = product_temperature
        self.driver_name = driver_name
        self.license_plate = license_plate
        self.created_by = created_by
        self.batch_code = batch_code
        self.origin = origin
        self.product_temp = product_temp
        self.kill_date = kill_date
        self.use_by = use_by
        self.slaughter_number = slaughter_number
        self.cut_number = cut_number
        self.red_tractor = red_tractor
        self.rspca = rspca
        self.organic_assured = organic_assured
        self.supplier = supplier
