package org.androidtown.joystickapp3;

/**
 * Created by 이경근 on 2017-03-21.
 */

public class Singleton{


    private static Singleton singleton = new Singleton();
    public static Singleton getInstance(){
        return singleton;
    }
    private Singleton(){

    }

}