//
//  Protocol.swift
//  prueba5
//
//  Created by Alejandro Nieto Alarcon on 13/05/2020.
//  Copyright © 2020 Alejandro Nieto Alarcon. All rights reserved.
//

import Foundation

class Protocol {
    
    private var clientThread : ClientThread!
    
    init(clientThread: ClientThread){
        self.clientThread = clientThread
    }
    
    /**
    * @brief Get the current time.
    * @return the current time.
    */
    private func getDateTime() -> String {
        let dateFormatter : DateFormatter = DateFormatter()
        //  dateFormatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
        dateFormatter.dateFormat = "yyyy-MMM-dd HH:mm:ss"
        let date = Date()
        let dateString = dateFormatter.string(from: date)
        //let interval = date.timeIntervalSince1970
        
        return String(dateString)
    }
    
    /**
    * @brief Proccess all the devices received by the server to display the information in the recycler view of the LoggedActivity
    * @pre The login has to been successful
    * @param inputline which is the data received from server with all the devices information
    * @return Returns one arraylist with the objects of the information received.
    */
    public func processDevices(from_client: String) -> [Device] {
        var allDevices = [Device]()
        let devices = from_client.split(separator: "#")
               
        var contador = 0
        var contador2 = 0
       
        var id_device = ""
        var device_name = ""
        var state = ""
        var maintenance = ""
       
        for row in devices {
            if(contador > 5){
               
                if contador2 == 1 {
                    id_device = String(row)
                }
               
                if contador2 == 2 {
                    device_name = String(row)
                }
               
                if contador2 == 3 {
                    state = String(row)
                }
               
                if contador2 == 4 {
                    maintenance = String(row)
                }
               
                if (row.contains("DEVICE") || row.contains("END")) && contador2 >= 4 && id_device != "" {
                    contador2 = 0
                    //print("Device --> " + id_device + " " + device_name + " " + state + " " + maintenance)
                    let aux = Device(id: id_device, identifier_name: device_name, state: state, maintenance: maintenance)
                    allDevices.append(aux)
                    id_device = ""
                    device_name = ""
                    state = ""
                    maintenance = ""
                }
               
                contador2 += 1

            }
            contador += 1
        }
        
        return allDevices
    }
    
    /**
    * @brief Compounds the protocol to try to get logged into the application
    * @param login which is the login of the person who wants to get logged
    * @param password which is the password of the user who wants to get logged
    * @return Returns the protocol to try to get logged
    */
    public func sendLogin(login: String, password: String) -> String {
        let output = "PROTOCOLTFG#" + self.getDateTime() + "#CLIENT#APPLE#LOGIN" + login + "#" + password + "#END"
        return output
    }
    
    /**
    * @brief Compounds the protocol to open a device with its id
    * @param id which is the id of the device we want to open
    * @return Returns the protocol to open a device
    */
    public func sendOpenDevice(id_device: Int) -> String{
        let tfg = "PROTOCOLTFG#"
        let fecha = self.getDateTime()
        let client = "#CLIENT#APPLE#"
        let open =  self.clientThread.getThreadOwner() + "#OPENDEVICE#" + String(id_device) + "#END";
        let output = tfg + fecha + client + open
        
        return output
    }
    
    /**
    * @brief Compounds the protocol to close a device with its id
    * @param id which is the id of the device we want to close
    * @return Returns the protocol to close a device
    */
    public func sendCloseDevice(id_device: Int) -> String {
        let tfg = "PROTOCOLTFG#"
        let fecha = self.getDateTime()
        let client = "#CLIENT#APPLE#"
        let open =  self.clientThread.getThreadOwner() + "#CLOSEDEVICE#" + String(id_device) + "#END";
        let output = tfg + fecha + client + open
        
        return output
    }
    
    /**
    * @brief Compounds the protocol to get logout into the application
    * @pre The user has to been logged previously
    * @return Returns the protocol to get logout
    */
    public func sendLogout() -> String {
        let output = "PROTOCOLTFG#" + self.getDateTime() + "#CLIENT#APPLE#LOGOUT#" + self.clientThread.getThreadOwner() + "#END";
        return output
    }
    
    /**
    * @brief Compounds the protocol to get the photo of one device
    * @param id which is the id of the device we want to get the photo
    * @return Returns the protocol to get the device photo
    */
    public func getPhoto(id_device: Int) -> String {
        let output = "PROTOCOLTFG#" + self.getDateTime() + "#CLIENT#APPLE#" + self.clientThread.getThreadOwner() + "#GETPHOTO#" + String(id_device) + "#END";
        return output
    }
}
