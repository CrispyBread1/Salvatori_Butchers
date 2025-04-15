class User:
    def __init__(self, id, created_at, name, department, permissions, email):
        self.approved = False
        self.id = id
        self.created_at = created_at
        self.name = name
        self.email = email
        self.department = department
        self.permissions = permissions

  
