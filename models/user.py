class User:
    def __init__(self, id, created_at, name, department, permissions, email, approved):
        self.id = id
        self.approved = approved
        self.created_at = created_at
        self.name = name
        self.email = email
        self.department = department
        self.permissions = permissions

  
