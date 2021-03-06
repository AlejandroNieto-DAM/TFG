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
    
    var mainViewController: ViewController!
    var loggedViewController: LoggedViewController!
    
    var threadOwner: String!
    
    var allDevices: [Device]
    var decodedData: Data!
    var imagePhotoIndex: Int!
    
    var mProtocol: Protocol!
    
    var listening = true
    
    /**
    * @brief Constructor
    * @param mainActivity which is the mainactivity in which this class has been instanciated
    */
    init() {
        allDevices = [Device]()
        imagePhotoIndex = 0
        decodedData = Data()
        mProtocol = Protocol(clientThread: self)
    }

    /**
    * @return Returns the threadOwner
    */
    func getThreadOwner() -> String {
        return self.threadOwner
    }
    
    /**
    * @brief Set the ViewController to this class
    * @param mainViewController which is the first screen
    * @pre The login has to been sucessful
    */
    func setViewController(mainViewController: ViewController){
        self.mainViewController = mainViewController
    }
    
    /**
    * @brief Set the LoggedViewController to this class
    * @param loggedViewController which is the second screen
    * @pre The login has to been sucessful
    */
    func setLoggedViewController(loggedViewController: LoggedViewController){
        self.loggedViewController = loggedViewController
    }
    
    /**
    * @brief Start the socket connection and start to listen to the server
    * @pre The server has to be up to get connected with this socket
    * @post This app will be listening to the socket and with the possibility to send data to the server
    */
    func startConnection() {
        
        var readStream: Unmanaged<CFReadStream>?
        var writeStream: Unmanaged<CFWriteStream>?

        CFStreamCreatePairWithSocketToHost(kCFAllocatorDefault, "192.168.1.135" as CFString, 12345, &readStream, &writeStream)
        
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
            while self.listening {
                let bytesRead = self.inputStream.read(&buffer, maxLength: bufferSize)
                
                if bytesRead > 0 {
                    let output = NSString(bytes: &buffer, length: bytesRead, encoding: String.Encoding.utf8.rawValue)
                    self.processInput(from_client: output!)
                } else {
                    
                }
            }

            
        }
    }
    
    /**
    * @brief procces the message received by the server to see if it have all the conditions to know if the message is real
    * @param from_client is the message received by the server
    * @pre the socket has to been connected
    */
    func processInput(from_client: NSString){
        
        let from_clientS = String(from_client)
        print("Lo que llega " + from_clientS)
        
        if from_clientS.contains("TOTAL") {
            //print("Received puertas")
            self.receiveDevices(from_client: from_clientS)
            self.mainViewController.startsSecondActivity()
            if self.allDevices.count > 0 {
                //self.getPhoto(id_device: self.allDevices[0].getID())
            }
            
        }
        else if from_clientS.contains("OPENINGDEVICE"){
            
            self.openDevice(from_client: from_clientS)
            
        } else if from_clientS.contains("CLOSINGDEVICE"){

            self.closeDevice(from_client: from_clientS)
            
        } else if from_clientS.contains("PHOTO"){

            self.processPhoto(from_client: from_clientS)
            
        }else if from_clientS.contains("FINIMAGE"){

            self.loadImage()
            
        }
        
        
    }
    
    /**
    * @brief Forms a image with the bytes previous received and if there is more devices to get their photo arms the protocol to send the msg to the server
    * @pre the socket has to been connected
    * @post the image finished will be set on the corresponding device
    */
    func loadImage(){
        
        let image = UIImage(data: self.decodedData)!
        if self.imagePhotoIndex == (self.allDevices.count - 1) {
            self.allDevices[self.allDevices
                .count - 1].setImage(image: image)
            //self.mainViewController.startsSecondActivity()
        } else {
            self.allDevices[self.imagePhotoIndex].setImage(image: image)
            self.imagePhotoIndex += 1
            self.decodedData.removeAll()
            self.getPhoto(id_device: self.allDevices[self.imagePhotoIndex].getID())
        }

    }
    
    /**
    * @brief Process the message received by the server with 512 bytes of the photo and ads it to the previous bytes.
    * @param from_client is the message received by the server in which there are 512 bytes of the photo
    * @pre the socket has to been connected
    * @post one photo will be formed with all the bytes
    * @throws IOException
    */
    func processPhoto(from_client: String){
        
        let sttms = from_client.split(separator: "#")
        
        var first = 0
        var second = 0
        
        let index = sttms[4].range(of: "b\'")?.lowerBound
        let distance = sttms[4].distance(from: sttms[4].startIndex, to: index!)
        first = distance + 3
        
        let index2 = sttms[4].range(of: "\r\n")?.lowerBound
        let distance2 = sttms[4].distance(from: sttms[4].startIndex, to: index2!)
        second = first + distance2
        second = second - 4
                
        let decode = Data(base64Encoded: String(sttms[4]).substring(with: 2..<second))!
        self.decodedData.append(contentsOf: decode)
        
    }
    
    /**
    * @brief Sends to the server the message with the protocol to try to get logged
    * @param login is the login of the user who wants to get logged
    * @param password which is the password of the user who wants to get logged
    * @pre the socket has to been connected
    * @post if the login is successful the apps goes to the next application
    */
    func sendLogin(login: String, password: String) {
        self.threadOwner = login
        let output = self.mProtocol.sendLogin(login: login, password: password)
        self.sendMsg(output: output)
    }
    
    /**
    * @brief Send the message to open a specific device to the server
    * @param id_device which is the id of the device we want to open
    * @pre the socket has to been connected
    * @post if its possible the specific device will be opened
    */
    func sendOpenDevice(id_device: Int){
        let output = self.mProtocol.sendOpenDevice(id_device: id_device)
        self.sendMsg(output: output)
    }
    
    /**
    * @brief Send the message to close a specific device to the server
    * @param id_device  which is the id of the device we want to close
    * @pre the socket has to been connected
    * @post if its possible the specific device will be closed
    */
    func sendCloseDevice(id_device: Int){
        let output = self.mProtocol.sendCloseDevice(id_device: id_device)
        self.sendMsg(output: output)
    }
    
    /**
    * @brief Sends the param msg by the socket to the server
    * @param output is the msg that will be sent to the server
    * @pre the socket has to been connected
    * @post the server will return an answer
    */
    func sendMsg(output: String){
        outputStream.write(output, maxLength: output.count)
    }
    
    /**
    * @return Returns all the devices
    */
    func getAllDevices() -> [Device]{
        return self.allDevices
    }
    
    /**
    * @brief Process the message of the server that says that one door was opened
    * @param from_client which is the message received by the server with the id of the opened device
    * @pre the socket has to been connected
    * @post the data of the recycler view in the LoggedActivity will be updated with the new value
    */
    func openDevice(from_client: String){
        
        let sttms = from_client.split(separator: "#")
        
        for device in allDevices {
            if String(device.getID()) == sttms[4] {
                device.setState(state: "1")
            }
        }
        
        self.loggedViewController.refresh()
    }
    
    /**
    * @brief Process the message of the server that says that one door was closed
    * @param from_client which is the message received by the server with the id of the closed device
    * @pre the socket has to been connected
    * @post the data of the recycler view in the LoggedActivity will be updated with the new value
    */
    func closeDevice(from_client: String){
        
        let sttms = from_client.split(separator: "#")
        
        for device in allDevices {
            if String(device.getID()) == sttms[4] {
                device.setState(state: "0")
            }
        }
        
        self.loggedViewController.refresh()
    }
    
    /**
    * @brief Sends a message to the server to start receiving the photo of the specific device
    * @param id_device which is the id of the device we want to get the photo
    */
    func getPhoto(id_device: Int){
        let output = self.mProtocol.getPhoto(id_device: id_device)
        sendMsg(output: output)
    }
    
    /**
    * @brief Process the devices received to load it in one array and generates the protocol to get the first device image
    * @param from_client which is the message received by the server with all the devices
    * @pre the socket has to been connected
    */
    func receiveDevices(from_client: String){
        self.allDevices = self.mProtocol.processDevices(from_client: from_client)
    }
    
    func sendLogout(){
        let output = self.mProtocol.sendLogout()
        self.sendMsg(output: output)
    }
    
    func setFinished(){
        self.listening = false
    }
}
