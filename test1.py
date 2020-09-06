from Box_Ball import *

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
    gate_A=Gate("A",[325,400])
    gate_list.append(gate_A)

    #gate B
    gate_B=Gate("B",[475,400])
    gate_list.append(gate_B)

    #box agent 1
    box_agent_A=Box_agents("A",[25,25],[20,330],[20,380],RED)
    box_agent_list.append(box_agent_A)

    #box agent 2
    box_agent_B=Box_agents("B",[765,25],[470,780],[20,380],RED)
    box_agent_list.append(box_agent_B)

    '''as of now only single ball is there, so no need to be careful on naming and gate-ball relationships. 1 ball, 2 gate'''
    #ball_agent
    agent_guard_gates=gate_list
    ball_agent_1=Ball_agent("1",[400,750],agent_guard_gates,MAROON)
    ball_agent_list.append(ball_agent_1)

    block_ratio_dict = gate_ball_len_ratio(gate_list, ball_agent_list, box_agent_list)
    running=True


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
            box_agent.move_box()

        for gate in gate_list:
            gate.draw_gate()

        for ball_agent in ball_agent_list:
            ball_agent.move_ball(box_agent_list,block_ratio_dict)


        clock.tick(60)
        pygame.display.flip()

        '''no ending condition is defined. ruuning is always TRUE'''


game()
