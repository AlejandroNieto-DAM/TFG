//
//  ClientThread.swift
//  prueba5
//
//  Created by Alejandro Nieto Alarcon on 12/05/2020.
//  Copyright © 2020 Alejandro Nieto Alarcon. All rights reserved.
//

import Foundation
import UIKit

class ClientThread {
    
    var inputStream: InputStream!
    var outputStream: OutputStream!
    
    var allDevices = [Device]()
    
    var mainViewController: ViewController!
    var loggedViewController: LoggedViewController!
    
    var threadOwner: String!
    
    var image = [UInt8]()
    var decodedData = Data()
    
    var imagePhotoIndex = 0

    func setViewController(mainViewController: ViewController){
        self.mainViewController = mainViewController
    }
    
    func setLoggedViewController(loggedViewController: LoggedViewController){
        self.loggedViewController = loggedViewController
    }
    
    func startConnection() {
        
        var readStream: Unmanaged<CFReadStream>?
        var writeStream: Unmanaged<CFWriteStream>?

        CFStreamCreatePairWithSocketToHost(kCFAllocatorDefault, "192.168.1.135" as CFString, 12345, &readStream, &writeStream)
        
     //   Stream.getStreamsToHost(withName: "192.168.1.135", port: 12345, inputStream: &self.inputStream, outputStream: &self.outputStream)

        
        inputStream = readStream?.takeRetainedValue()
        outputStream = writeStream?.takeRetainedValue()
        
        inputStream?.schedule(in: .current, forMode: .default)
        outputStream?.schedule(in: .current, forMode: .default)
        
        inputStream?.open()
        outputStream?.open()
        
                    
        DispatchQueue.global(qos: .background).async {
            let bufferSize = 1024
            var buffer = Array<UInt8>(repeating: 0, count: bufferSize)
            
            //Resolver el bug conexion socket se corta al minuto y medio
            while true {
                let bytesRead = self.inputStream.read(&buffer, maxLength: bufferSize)
                
                if bytesRead > 0 {
                    let output = NSString(bytes: &buffer, length: bytesRead, encoding: String.Encoding.utf8.rawValue)
                    self.processInput(from_client: output!)
                } else {
                    
                }
            }

            
        }
    }
    
    
    func processInput(from_client: NSString){
        
        let from_clientS = String(from_client)
        print("Lo que llega " + from_clientS)
        
        if from_clientS.contains("TOTAL") {
            print("Received puertas")
            self.receiveDevices(from_client: from_clientS as? String ?? "")
            
            if self.allDevices.count > 0 {
                self.getPhoto(id_device: self.allDevices[0].getID())
            }
            
        }
        else if from_clientS.contains("OPENINGDEVICE"){
            
            self.openDevice(from_client: from_clientS as? String ?? "")
            
        } else if from_clientS.contains("CLOSINGDEVICE"){

            self.closeDevice(from_client: from_clientS as? String ?? "")
            
        } else if from_clientS.contains("PHOTO"){

            self.processPhoto(from_client: from_clientS as? String ?? "")
            
        }else if from_clientS.contains("FINIMAGE"){

            self.loadImage()
            
        }
        
        
    }
    
    func loadImage(){
        
        let image = UIImage(data: self.decodedData)!
        if self.imagePhotoIndex == (self.allDevices.count - 1) {
            self.allDevices[self.allDevices
                .count - 1].setImage(image: image)
            self.mainViewController.startsSecondActivity()
        } else {
            self.allDevices[self.imagePhotoIndex].setImage(image: image)
            self.imagePhotoIndex += 1
            self.decodedData.removeAll()
            self.getPhoto(id_device: self.allDevices[self.imagePhotoIndex].getID())
        }

    }
    
    func processPhoto(from_client: String){
        
        var sttms = from_client.split(separator: "#")
        
        var first = 0
        var second = 0
        
        let index = sttms[4].range(of: "b\'")?.lowerBound
        let distance = sttms[4].distance(from: sttms[4].startIndex, to: index!)
        first = distance + 3
        
        let index2 = sttms[4].range(of: "\r\n")?.lowerBound
        let distance2 = sttms[4].distance(from: sttms[4].startIndex, to: index2!)
        second = first + distance2
        second = second - 4
        
        let yeyo = String(sttms[4])
        
        
        let decode = Data(base64Encoded: String(sttms[4]).substring(with: 2..<second))!
        self.decodedData.append(contentsOf: decode)
        
    }
    
    func sendLogin(login: String, password: String) {
        self.threadOwner = login
        let output = "PROTOCOLTFG#FECHA#CLIENT#APPLE#LOGIN" + login + "#" + password + "#END"
        self.sendMsg(output: output)
    }
    
    func sendOpenDevice(id_device: Int){
        
        
        let tfg = "PROTOCOLTFG#"
        let fecha = "FECHAHORA"
        let client = "#CLIENT#APPLE#"
        let open =  self.threadOwner + "#OPENDEVICE#" + String(id_device) + "#END";
        let output = tfg + fecha + client + open
        self.sendMsg(output: output)
        
    }
    
    func sendCloseDevice(id_device: Int){
        
        let tfg = "PROTOCOLTFG#"
        let fecha = "FECHAHORA"
        let client = "#CLIENT#APPLE#"
        let open =  self.threadOwner + "#CLOSEDEVICE#" + String(id_device) + "#END";
        let output = tfg + fecha + client + open
        self.sendMsg(output: output)
    }
    
    func sendMsg(output: String){
        outputStream.write(output, maxLength: output.count)
    }
    
    func getAllDevices() -> [Device]{
        return self.allDevices
    }
    
    func openDevice(from_client: String){
        
        var sttms = from_client.split(separator: "#")
        
        for device in allDevices {
            if String(device.getID()) == sttms[4] {
                device.setState(state: "1")
            }
        }
        
        self.loggedViewController.refresh()
    }
    
    func closeDevice(from_client: String){
        
        var sttms = from_client.split(separator: "#")
        
        for device in allDevices {
            if String(device.getID()) == sttms[4] {
                device.setState(state: "0")
            }
        }
        
        self.loggedViewController.refresh()
    }
    
    func getPhoto(id_device: Int){
        var output = "PROTOCOLTFG#" + "FECHAHORA" + "#CLIENT#APPLE#" + self.threadOwner + "#GETPHOTO#" + String(id_device) + "#END";
        sendMsg(output: output)
    }
    
    func receiveDevices(from_client: String){
        
        var devices = from_client.split(separator: "#")
        
        //TODO substring and index of the chain
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
                    print("Device --> " + id_device + " " + device_name + " " + state + " " + maintenance)
                    let aux = Device(id: id_device, identifier_name: device_name, state: state, maintenance: maintenance)
                    self.allDevices.append(aux)
                    id_device = ""
                    device_name = ""
                    state = ""
                    maintenance = ""
                }
                
                contador2 += 1
 
            }
            contador += 1
        }
        
    }
    
    
}
