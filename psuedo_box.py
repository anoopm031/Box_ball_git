class Psuedo_box:
    def __init__(self,name,position,velocity,acceleration):
        self.name=name
        self.position=position
        self.x_vel=velocity[0]
        self.y_vel=velocity[1]
        self.z_vel=velocity[2]
        self.x_acc=acceleration[0]
        self.y_acc=acceleration[1]
        self.z_acc=acceleration[2]

    def update_info(self,position,velocity,acceleration):
        self.position=position
        self.x_vel=velocity[0]
        self.y_vel=velocity[1]
        self.z_vel=velocity[2]
        self.x_acc=acceleration[0]
        self.y_acc=acceleration[1]
        self.z_acc=acceleration[2]

    def predict_new_pos(self):
        self.position[0]=self.position[0]+self.x_vel+0.5*self.x_acc
        self.position[1]=self.position[1]+self.y_vel+0.5*self.y_acc
        self.position[2]=self.position[2]+self.z_vel+0.5*self.z_acc

