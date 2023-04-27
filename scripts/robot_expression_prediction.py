#!/usr/bin/env python

from __future__ import print_function

import rospy
from cr_week6_test.srv import *

def handle_compute(req):

    params = req.params
    # Bayesian Network implementation

    robot_id = params.id
    OS = params.object_size
    HA = params.human_action
    HE = params.human_expression

    # Making all input data a string
    index = str(HE) + str(HA)+ str(OS)

    # Dictionary of lists to represent conditonal prob table
    prob_dict = {
        "111": [0.8, 0.2, 0.0],
        "112": [1.0, 0.0, 0.0],
        "121": [0.8, 0.2, 0.0],
        "122": [1.0, 0.0, 0.0],
        "131": [0.6, 0.2, 0.2],
        "132": [0.8, 0.2, 0.0],
        "211": [0.0, 0.0, 1.0],
        "212": [0.0, 0.0, 1.0],
        "221": [0.0, 0.1, 0.9],
        "222": [0.1, 0.1, 0.8],
        "231": [0.0, 0.2, 0.8],
        "232": [0.2, 0.2, 0.6],
        "311": [0.7, 0.3, 0.0],
        "312": [0.8, 0.2, 0.0],
        "321": [0.8, 0.2, 0.0],
        "322": [0.9, 0.1, 0.0],
        "331": [0.6, 0.2, 0.2],
        "332": [0.7, 0.2, 0.1],
        "Nil": [0.0, 0.0, 0.0]
    }



    # If all variables are known
    if index.count('0') == 0:
        p_h = prob_dict[index][0]
        p_s = prob_dict[index][1]
        p_n = prob_dict[index][2]

    # If one variable is unknown
    elif index.count('0') == 1:
        if index[0] == '0' or index[1] == '0':  # When unknown is either HA or HE
            index_1 = index.replace('0', '1') # Prob when HA or HE = 1
            index_2 = index.replace('0', '2') # Prob when HA or HE = 2
            index_3 = index.replace('0', '3') # Prob when HA or HE = 3
            prior_prob = 1/3
        
        else:     # When unknown is O
            index_1 = index.replace('0', '1') # Prob when O = 1
            index_2 = index.replace('0', '2') # Prob when O = 2
            index_3 = "Nil"
            prior_prob = 1/2
    
        # Using law of total probabilities to calculate prob
        p_h = (prob_dict[index_1][0] * prior_prob) + (prob_dict[index_2][0] * prior_prob) + (prob_dict[index_3][0] * prior_prob)
        p_s = (prob_dict[index_1][1] * prior_prob) + (prob_dict[index_2][1] * prior_prob) + (prob_dict[index_3][1] * prior_prob)
        p_n = (prob_dict[index_1][2] * prior_prob) + (prob_dict[index_2][2] * prior_prob) + (prob_dict[index_3][2] * prior_prob)

    # If two or all variables are unknown
    elif index.count('0') == 2 or index.count('0') == 3:
        #final_list = []
        # Empty list to save the probability of the robot expressions for each scenario
        p_ha = []
        p_sa = []
        p_ne = []
        prior_prob_3 = 1
        if index[2] != '0':  # If O is the known variable
            list_a = ['1', '2', '3']
            list_b = ['1', '2', '3']
            list_c = []
            list_c.append(index[2])
        
            prior_prob_1 = 1/3
            prior_prob_2 = 1/3
        
        elif index[1] != '0':  # If HA is the known variable
            list_a = ['1', '2', '3']
            list_b = []
            list_c = ['1', '2']
            list_b.append(index[1])
        
            prior_prob_1 = 1/3
            prior_prob_2 = 1/2
        
        elif index[0] != '0': # If HE is the known variable
            list_a = []
            list_b = ['1', '2', '3']
            list_c = ['1', '2']
            list_a.append(index[0])
        
            prior_prob_1 = 1/3
            prior_prob_2 = 1/2

        else: # For when all variables are zero
            list_a = ['1', '2', '3']
            list_b = ['1', '2', '3']
            list_c = ['1', '2']
            prior_prob_1 = 1/3
            prior_prob_2 = 1/3
            prior_prob_3 = 1/2
        
        # Using a for loop to get all possible scenarios and using law of total probabilities to calculate prob
        for HE in list_a:
            for HA in list_b:
                for O in list_c:
                    string = HE + HA + O
                    #final_list.append(string)
                    ph = prob_dict[string][0] * prior_prob_1 * prior_prob_2 * prior_prob_3
                    p_ha.append(ph)
                    ps = prob_dict[string][1] * prior_prob_1 * prior_prob_2 * prior_prob_3
                    p_sa.append(ps)
                    pn = prob_dict[string][2] * prior_prob_1 * prior_prob_2 * prior_prob_3
                    p_ne.append(pn)
        p_h = sum(p_ha)
        p_s = sum(p_sa)
        p_n = sum(p_ne)
    
    else:
        print('Wrong Variable values were given')

    
    #print('%s, %.3f, %.3f, %.3f' % (index, p_h, p_s, p_n))
    

    return predict_robot_expressionResponse(p_h, p_s, p_n)

def robot_control():
    # Initialise node
    rospy.init_node('robot_control')

    # initialise service
    s = rospy.Service('robot_prediction', predict_robot_expression, handle_compute)

    print("Ready to compute")

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == "__main__":
    robot_control()