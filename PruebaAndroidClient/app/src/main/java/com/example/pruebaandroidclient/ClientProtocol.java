package com.example.pruebaandroidclient;

import android.util.Log;

import java.util.ArrayList;

public class ClientProtocol {

    public ArrayList proccesDoors(String inputline){
        ArrayList<Door> doors = new ArrayList<>();

        String[] splittedDoors = inputline.substring(inputline.indexOf("DOOR")).split("#");

        //PROTOCOLTFG#SERVER#FECHA#TOTALDOORS#4#DOOR#id#nombre#estado#enmantenimiento#END

        int index = 0;
        int idDoor = 0;
        String doorName = "";
        int state = 0;
        int maintenance = 0;
        for(String s: splittedDoors){

            if(index == 1){
                idDoor = Integer.parseInt(s);
            }

            if(index == 2){
                doorName = s;
            }

            if(index == 3){
                state = Integer.parseInt(s);
            }

            if(index == 4){
                maintenance = Integer.parseInt(s);
            }

            if((s.equals("DOOR") || s.equals("END")) && index >= 4 ){
                index = 0;
                Log.i("Mira una door -->", idDoor + " "  + doorName  + " "  + state  + " "  +  maintenance);
                Door auxiliar = new Door(idDoor, doorName, state, maintenance, "");
                doors.add(auxiliar);
                idDoor = 0;
                doorName = "";
                state = 0;
                maintenance = 0;
            }

            Log.i("Mira por donde  -->", s + " " + index );
            index++;


        }

        return doors;
    }
}
