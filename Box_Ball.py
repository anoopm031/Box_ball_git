import pygame
import math
import random

pygame.init()

WIDTH=800
HEIGHT=800
SCRN_CLR=(0,0,0)
color=(255,0,0)
ground=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Box_Ball")
gate_list=[]
box_agent_list=[]
ball_agent_list=[]
obstruction_list=[]
SCALE=10
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
BLACK=(0,0,0)
WHITE=(255,255,255)
MAROON=(150,20,120)
clock=pygame.time.Clock()



#randomly moving agents
class Box_agents:
    def __init__(self,name,x_lim,y_lim,x_spawn_lim,y_spawn_lim,gate_position,color):
        '''position should be a list'''
        self.name=name
        self.ini_position=[random.choice(range(x_spawn_lim[0],x_spawn_lim[1])),random.choice(range(y_spawn_lim[0],y_spawn_lim[1])),0] #gives the initialisation position
        self.position=self.ini_position
        self.req_gate_position=gate_position
        self.color=color
        self.size=30
        self.x_lim=x_lim                           #movable area for the agent. x coordinates
        self.y_lim=y_lim                             #movable area for the agent. y coordinates
        self.z_lim=[0,0]
        self.movable=True

        '''slope of line joining box_initial position and gate'''
        slope=(self.ini_position[1]-self.req_gate_position[1])/(self.ini_position[0]-self.req_gate_position[0])

        if slope>=0:
            self.x_vel = random.uniform(1, 2)/100
            self.x_acc = random.uniform(0, 2)/10000
        else:
            self.x_vel = -random.uniform(1, 2) / 100
            self.x_acc = -random.uniform(0, 2) / 10000
            #print(f"x_vel_2,x_acc= {self.x_vel},{self.x_acc}")
        self.y_vel=slope*self.x_vel     #so that box will always head towards gate
        self.y_acc = slope * self.x_acc
        self.z_vel=0
        self.z_acc=0
        print(f"ini_position {self.ini_position}, slope {slope}, x_vel {self.x_vel}, y_vel {self.y_vel}, x_acc {self.x_acc}, y_acc {self.y_acc}")
        '''each call of move_box_new will be considered synonym to passing of time'''
        self.time_lapsed=0
        #this will be incremented appropriately in move_box_new method


    def move_box(self):
        x_vel=random.choice(range(-10,11))
        y_vel=random.choice(range(-10,12))      #adjusting this range can adjust the approach time of agents to gates
        x_new=self.position[0]+x_vel
        y_new=self.position[1]+y_vel

        '''checking the boundary'''
        if x_new>self.x_lim[0] and x_new<self.x_lim[1] and y_new>self.y_lim[0] and y_new<self.y_lim[1]:
            self.position[0]=x_new
            self.position[1]=y_new
        else:
            '''again generating a random vel if the box went out of boundary in the previous try'''
            self.move_box()
        '''drawing the box. Image blitting can also be used'''
        pygame.draw.rect(ground,self.color,pygame.Rect(self.position[0],self.position[1],30,30))

    def move_box_new(self):
        '''checking boundary'''
        if math.sqrt(((self.position[0]-self.req_gate_position[0])**2)+((self.position[0]-self.req_gate_position[0])**2)) >5:
           pass
        else:
            self.movable=False
        if self.movable:
            self.position[0]+=(self.x_vel*self.time_lapsed)+(0.5*self.x_acc*self.time_lapsed*self.time_lapsed)
            self.position[1]+=(self.y_vel*self.time_lapsed)+(0.5*self.y_acc*self.time_lapsed*self.time_lapsed)
            self.position[2]=0
            self.time_lapsed+=1
            pygame.draw.rect(ground, self.color, pygame.Rect(self.position[0], self.position[1], 30, 30))
        else:
            pygame.draw.rect(ground, self.color, pygame.Rect(self.req_gate_position[0], self.req_gate_position[1], 30, 30))


    def get_vel(self):
        return [self.x_vel,self.y_vel,self.z_vel] #returns a list


    def get_position(self):
        return self.position #returns a list


#agants that moves following a calculation. Guarding agents
class Ball_agent:
    def __init__(self,name,position,agent_guarding_gates_list,color):
        #position should be a list
        self.name=name
        self.ini_position=position #initial position of the ball. Used for calcutlating length_ratio
        self.position=position
        self.color=color
        self.size=10
        self.guarding_gates=agent_guarding_gates_list   #the gates guarded by the ball, It should be 2. 2 gates per ball for now
        self.length_ratio=0


    def set_move_ratio(self,len_ratio):
        '''setting the length_ratio'''
        self.length_ratio=len_ratio
        return 1

    '''to find the real-time distance between gate and box'''
    def move_ball(self,box_agent_list, block_ratio_dict):
        '''block_ratio_dict contains length_ratios'''
        gate_arc_list=[]   #list containing radiuses
        for gate, box, block_ratio in zip(self.guarding_gates, box_agent_list, block_ratio_dict.values()):
            #print(gate.name,box.name)
            if box.name == gate.name:
                distance = math.sqrt(
                    (box.position[0] - gate.position[0]) ** 2 + (box.position[1] - gate.position[1]) ** 2)
                gate_arc = distance / block_ratio
                gate_arc_list.append(gate_arc)


        '''to draw the intersecting circles that's being used for movement of ball'''

        for gate_arc_length,gate in zip(gate_arc_list,self.guarding_gates):
            '''draw arcs with each length, find intersections, and check whether that exists and if exists
            #if exists, whether or not inside the balls allowed movement area'''

            try:
                pygame.draw.circle(ground,RED,gate.position,int(gate_arc_length),1)
            except:
                break
            pass

        '''distance between two gates'''
        gates_distance=math.sqrt((self.guarding_gates[0].position[0]-self.guarding_gates[1].position[0])**2+(self.guarding_gates[0].position[1]-self.guarding_gates[1].position[1])**2)
        '''checking whether circles overlap or not'''
        overlapping=self.check_intersection(gate_arc_list,gates_distance)
        #print(f"overlapping is {overlapping}")

        if overlapping:
            '''find out the overlapping points and find out the one that's lying inside the balls movement area.
            #solve two circles two find out the intersection points'''
            intersection_1, intersection_2 = self.find_intersection(gate_arc_list)
            for intersection in intersection_1,intersection_2:
                if self.check_boundary(intersection):
                    self.position[0]=round(intersection[0])
                    self.position[1]=round(intersection[1])
                    break

        else:
            closest_box_arc=min(gate_arc_list)
            closest_gate=gate_arc_list.index(closest_box_arc)
            if closest_gate==0:
                rangemin=300
                rangemax=self.guarding_gates[0].position[0]+closest_box_arc
            elif closest_gate==1:
                rangemin=self.guarding_gates[1].position[0]-closest_box_arc
                rangemax=500

            random_x = random.choice(range(round(rangemin), round(rangemax)))
            self.position=self.circle_y_points(random_x,closest_gate,closest_box_arc)

            '''a random x will be choosen from relevant area and will be subsituted in circle equation and find a self.position point
            #find out the rectangle that's enclosing the arc and select a random x or y and put in the closest_box_arc circle's equation
            #to find out the next position of the ball'''

        #print(self.position)
        pygame.draw.circle(ground, self.color,self.position, 10)
        pass

    def circle_y_points(self,x_pos,gate_no,radius):
        gate_position=self.guarding_gates[gate_no].position
        a,b=gate_position[0],gate_position[1]
        try:
            y1 = b + math.sqrt(radius ** 2 - (x_pos - a) ** 2)
        except:
            print("Domain error")
            y1=0
        try:
            y2 = b - math.sqrt(radius ** 2 - (x_pos - a) ** 2)
        except:
            print("Domain error")
            y2=0
        for y in y1,y2:
            if self.check_boundary([x_pos,round(y)]):
                return [x_pos,round(y)]
            else:
                return self.ini_position



    def check_intersection(self,gate_arc_list,gates_distance):
        overlapping=False
        radius_sum=gate_arc_list[0]+gate_arc_list[1]
        if gates_distance>abs(gate_arc_list[0]-gate_arc_list[1]):
            if gates_distance<radius_sum:
                overlapping=True

        return overlapping



    def find_intersection(self,gate_arc_list):
        #circle 1
        r1=gate_arc_list[0]
        center_1=self.guarding_gates[0].position
        a=center_1[0]
        b=center_1[1]
        #write the filter and find out the point when x when y=center_2_y


        #circle 2
        r2=gate_arc_list[1]
        center_2=self.guarding_gates[1].position
        c=center_2[0]
        d=center_2[1]
        #print("a,b,c,d",a,b,c,d)
        #write the filter and find out the point when x when y=center_2_y


        '''not using the below code as y1=y2 for our current case'''
        '''
        k1=(a-c)/(b-d)
        k2=(r1**2-r2**2-a**2-b**2+c**2+d**2)/(2*(b-d))

        A=k1**2+1
        B=2*k1*k2-2*k1-2*a
        C=a**2+k2**2+b**2-2**k2-r1**2

        x1=(-B+math.sqrt(B**2-4*A*C))/(2*A)
        x2=(-B-math.sqrt(B**2-4*A*C))/(2*A)
        print(f"x1,x2,={x1} ,{x2}")
        '''

        intersec_x=(a**2-c**2-r1**2+r2**2)/(2*(a-c))
        try:
            intersec_y1=b+math.sqrt(r1**2-(intersec_x-a)**2)
        except:
            intersec_y1=0
        try:
            intersec_y2=b-math.sqrt(r1**2-(intersec_x-a)**2)
        except:
            intersec_y2=0

        return [intersec_x,intersec_y1],[intersec_x,intersec_y2]

    def check_boundary(self,point):
        bound=False
        if point[0]>300 and point[0]<500:
            if point[1]>400 and point[1]<800:
                bound=True

        return bound



#obstructions, we can use different obstructions by scaling the image to our required resolution and blitting
class Obstruction:
    def __init__(self,position,width,height,ob_type,color):
        self.position=position
        self.x_width=width
        self.y_height=height
        self.ob_type=ob_type
        self.color=color


    def draw_obstruction(self):
        pygame.draw.rect(ground, self.color,pygame.Rect(self.position[0], self.position[1], self.x_width, self.y_height))
        return 1



class Gate:
    def __init__(self,name,position):
        self.position=position
        self.name=name

    def draw_gate(self):
        pygame.draw.circle(ground,GREEN,self.position,5)



def gate_ball_len_ratio(gate_list,ball_agent_list,box_agent_list):
    "ratio between distance between gate and box and gates and ball are taken for drawing the arcs and finding intersection"
    block_ratio_dict={}
    for gate in gate_list:
        for ball in ball_agent_list:
            ball_position = ball.ini_position
            gate_position = gate.position
            ball_gate_distance = math.sqrt((ball_position[0] - gate_position[0]) ** 2 + (ball_position[1] - gate_position[1]) ** 2)
            #ball_name=ball.name

        for box in box_agent_list:
            if box.name==gate.name:
                gate_position=gate.position
                box_position=box.ini_position
                box_gate_distance=math.sqrt((box_position[0]-gate_position[0])**2+(box_position[1]-gate_position[1])**2)

        #this part is simplified to fit
        ball_gate_len_ratio=box_gate_distance/ball_gate_distance
        gate_ball_name=f"{gate.name}_{ball.name}_len_ratio"
        block_ratio_dict[gate_ball_name]=ball_gate_len_ratio

    return block_ratio_dict

def end_game():
    pygame.quit()
    quit()
