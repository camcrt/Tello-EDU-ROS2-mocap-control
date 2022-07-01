#!/usr/bin/env python
# Save position in a .csv named pos.csv

import rospy
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def save():

    
    count = 0
    val = 0
    x = y = z = 0

   
    rospy.init_node('save_pose', anonymous=True)

    df = pd.read_csv('eggs.csv')

    count = len(df)

    ax = plt.axes(projection="3d")
    while val < count : 
        if val % 6 == 0:  
            ax.scatter (df.iloc[x,y+1],df.iloc[x,y + 2],df.iloc[x,y +3])
        x += 1 

        val +=1

    plt.show() 
   
    rospy.spin()

if __name__ == '__main__':
    save()