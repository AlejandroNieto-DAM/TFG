//
//  ClientThread.swift
//  prueba5
//
//  Created by Alejandro Nieto Alarcon on 12/05/2020.
//  Copyright © 2020 Alejandro Nieto Alarcon. All rights reserved.
//

import Foundation

class ClientThread {
    
    var inputStream: InputStream!
    var outputStream: OutputStream!
    
    var allDevices = [Device]()
    
    var mainViewController: ViewController!

    func setViewController(mainViewController: ViewController){
        self.mainViewController = mainViewController
    }
    
    func startConnection() {
        
        var readStream: Unmanaged<CFReadStream>?
        var writeStream: Unmanaged<CFWriteStream>?

        CFStreamCreatePairWithSocketToHost(kCFAllocatorDefault,
                                           "192.168.1.135" as CFString,
                                           12345,
                                           &readStream,
                                           &writeStream)
        
        inputStream = readStream!.takeRetainedValue()
        outputStream = writeStream!.takeRetainedValue()
        
        inputStream.schedule(in: .current, forMode: .common)
        outputStream.schedule(in: .current, forMode: .common)
        
        inputStream.open()
        outputStream.open()
        
                    
        DispatchQueue.global(qos: .background).async {
            let bufferSize = 1024
            var buffer = Array<UInt8>(repeating: 0, count: bufferSize)

            print("waintig for handshake...")
            
            let bytesRead = self.inputStream.read(&buffer, maxLength: bufferSize)
            if bytesRead >= 0 {
                let output = NSString(bytes: &buffer, length: bytesRead, encoding: String.Encoding.utf8.rawValue)
                self.processInput(from_client: output!)
            } else {
                
            }
            
        }
    }
    
    
    func processInput(from_client: NSString){
        
        let from_clientS = from_client
        print(from_client as? String)
        
        if from_clientS.contains("TOTAL") {
            print("Received puertas")
            self.receiveDevices(from_client: from_clientS as? String ?? "")
            self.mainViewController.startsSecondActivity()
        }
        else if from_clientS.contains("OPENDEVICE"){
            
        }
        
        
    }
    
    func sendLogin(login: String, password: String) {
        let output = "PROTOCOLTFG#FECHA#CLIENT#SWIFT#LOGIN" + login + "#" + password + "#END"
        self.sendMsg(output: output)
    }
    
    func sendMsg(output: String){
        outputStream.write(output, maxLength: output.count)
    }
    
    func getAllDevices() -> [Device]{
        return self.allDevices
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
