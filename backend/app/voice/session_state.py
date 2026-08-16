class SessionState:

    def __init__(self):
        self.customer_db_id = None
        self.customer_id = None
        self.customer_name = None
        self.verified = False

    def reset(self):
        self.customer_db_id = None
        self.customer_id = None
        self.customer_name = None
        self.verified = False