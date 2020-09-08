from Box_Ball import *
from psuedo_box import *

def populate_psuedo_box_list(box_agent_list):
    "creating psuedo box objects-should return a list with psuedo box agents"
    temp_psuedo=[]
    for box in box_agent_list:
        psuedo=Psuedo_box(box.name,box.position,(box.x_vel,box.y_vel,box.z_vel),(box.x_acc,box.y_acc,box.z_acc))
        temp_psuedo.append(psuedo)
    return temp_psuedo


def game():
    #obstruction 1
    obstruction_1=Obstruction((200,800),100,-400,"rect",BLUE)
    obstruction_list.append(obstruction_1)

    #obstruction 2
    obstruction_2=Obstruction((500,800),100,-400,"rect",BLUE)
    obstruction_list.append(obstruction_2)

    #obstruction 3
    obstruction_3=Obstruction((350,0),100,400,"rect",BLUE)
    obstruction_list.append(obstruction_3)

    #define gate w.r.t obstructions
    '''corresponding gates and and box should be named same. That's box.name should be same as gate.name for box-gate combo'''
    #gate A
    gate_A_pos=[325,400]
    gate_A=Gate("A",gate_A_pos)
    gate_list.append(gate_A)

    #gate B
    gate_B_pos = [475,400]
    gate_B=Gate("B",gate_B_pos)
    gate_list.append(gate_B)

    #box agent 1
    x_lim_1=[20,330]
    y_lim_1=[20,100]
    x_spawn_lim_1=[20,330]
    y_spawn_lim_1=[20,100]
    gate_position_1=gate_A.position
    color_1=RED
    box_agent_A=Box_agents("A",x_lim_1,y_lim_1,x_spawn_lim_1,y_spawn_lim_1,gate_position_1,color_1)
    box_agent_list.append(box_agent_A)

    #box agent 2
    x_lim_2=[470,780]
    y_lim_2=[20,100]
    x_spawn_lim_2=[470,780]
    y_spawn_lim_2=[20,100]
    gate_position_2=gate_B.position
    color_2=RED
    box_agent_B=Box_agents("B",x_lim_2,y_lim_2,x_spawn_lim_2,y_spawn_lim_2,gate_position_2,color_2)
    box_agent_list.append(box_agent_B)

    '''as of now only single ball is there, so no need to be careful on naming and gate-ball relationships. 1 ball, 2 gate'''
    #ball_agent
    agent_guard_gates=gate_list
    ball_agent_pos=[400,750]
    ball_agent_1=Ball_agent("1",ball_agent_pos,agent_guard_gates,MAROON)
    ball_agent_list.append(ball_agent_1)

    block_ratio_dict = gate_ball_len_ratio(gate_list, ball_agent_list, box_agent_list)
    running=True
    iter_no=0
    SENSOR_FREQUENCY=5
    psuedo_box_list=populate_psuedo_box_list(box_agent_list)

    while running:
        ground.fill(BLACK)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                end_game()
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                end_game()

        for obstruction in obstruction_list:
            obstruction.draw_obstruction()

        for box_agent in box_agent_list:
            box_agent.move_box_new()

        for gate in gate_list:
            gate.draw_gate()

        if iter_no/SENSOR_FREQUENCY==1:
            for box,psuedo_box in zip(box_agent_list,psuedo_box_list):
                psuedo_box.update_info(box.position,(box.x_vel,box.y_vel,box.z_vel),(box.x_acc,box.y_acc,box.z_acc))
        else:
            for psuedo_box in psuedo_box_list:
                psuedo_box.predict_new_pos()

        for ball_agent in ball_agent_list:
            ball_agent.move_ball(psuedo_box_list,block_ratio_dict)
            #ball_agent.move_ball(box_agent_list,block_ratio_dict)

        movable_boxes= sum(box.movable for box in box_agent_list)
        if movable_boxes==0:
            finished=True
            while finished:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end_game()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        end_game()

        clock.tick(60)
        pygame.display.flip()

        '''no ending condition is defined. ruuning is always TRUE'''


game()
