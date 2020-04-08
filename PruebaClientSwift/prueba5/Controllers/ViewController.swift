//
//  ViewController.swift
//  prueba5
//
//  Created by Alejandro Nieto Alarcon on 28/03/2020.
//  Copyright © 2020 Alejandro Nieto Alarcon. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    
    @IBOutlet weak var vmContainer:UIView!
    @IBOutlet weak var vmContainer2:UIView!
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var sendBtn: UIButton!
    @IBOutlet weak var usernameTextFld: UITextField!
    @IBOutlet weak var passTextFld: UITextField!
    
    
    @IBOutlet weak var loadingIndicator: UIActivityIndicatorView!
    
    var inputStream: InputStream!
    var outputStream: OutputStream!
    var username = ""
    let maxReadLength = 4096
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.setUpElements()
        

        
        
        /*
        
        let data = "viva willy"
        //print(Unmanaged.passUnretained(data).toOpaque())
        outputStream.write(data, maxLength: data.count)
        
        
        print("Que pasa feo")
        

        DispatchQueue.global(qos: .background).async {
            while true {
                let bufferSize = 1024
                var buffer = Array<UInt8>(repeating: 0, count: bufferSize)

                print("waintig for handshake...")
                
                let bytesRead = self.inputStream.read(&buffer, maxLength: bufferSize)
                if bytesRead >= 0 {
                    var output = NSString(bytes: &buffer, length: bytesRead, encoding: String.Encoding.utf8.rawValue)
                    print(output)
                } else {
                    // Handle error
                }
                
                
                self.outputStream.write(data, maxLength: data.count)
            }
        }*/
    }
    
    func setUpElements(){
        self.hideKeyboardWhenTappedAround()
        NotificationCenter.default.addObserver(self, selector: #selector(keyboardWillShow), name: UIResponder.keyboardWillShowNotification, object: nil)
        
        
        
        sendBtn.layer.cornerRadius = 15.0
        sendBtn.layer.backgroundColor = Colors.firstBlue.cgColor
        
        usernameTextFld.layer.cornerRadius = 15.0
        usernameTextFld.layer.borderColor = Colors.firstBlue.cgColor
        
        passTextFld.layer.cornerRadius = 15.0
        passTextFld.layer.borderColor = Colors.firstBlue.cgColor
        
        vmContainer.layer.cornerRadius = 50.0
        vmContainer.layer.shadowColor = UIColor.gray.cgColor
        vmContainer.layer.shadowOffset = .zero
        vmContainer.layer.shadowOpacity = 0.8
        vmContainer.layer.shadowRadius = 50.0
        vmContainer.layer.shadowPath = UIBezierPath(rect: vmContainer.bounds).cgPath
        vmContainer.layer.shouldRasterize = true
        
        vmContainer2.setGradientBackground(colorOne: Colors.firstBlue, colorTwo: Colors.secondBlue)
        vmContainer2.layer.cornerRadius = 50.0
        vmContainer2.layer.shouldRasterize = true
        
        var readStream: Unmanaged<CFReadStream>?
        var writeStream: Unmanaged<CFWriteStream>?

        // 2
        CFStreamCreatePairWithSocketToHost(kCFAllocatorDefault,
                                           "192.168.1.134" as CFString,
                                           1234,
                                           &readStream,
                                           &writeStream)
        
        inputStream = readStream!.takeRetainedValue()
        outputStream = writeStream!.takeRetainedValue()
        
        inputStream.schedule(in: .current, forMode: .common)
        outputStream.schedule(in: .current, forMode: .common)
        
        inputStream.open()
        outputStream.open()
    }
    
    
    @objc func keyboardWillShow(notification: NSNotification) {
        if let keyboardSize = (notification.userInfo?[UIResponder.keyboardFrameBeginUserInfoKey] as? NSValue)?.cgRectValue {
            if self.view.frame.origin.y == 0 {
                self.view.frame.origin.y -= keyboardSize.height /  2
            }
        }
    }

    
    
    func hideKeyboardWhenTappedAround() {
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(dismissKeyboard))
        tap.cancelsTouchesInView = false
        view.addGestureRecognizer(tap)
    }

    @objc func dismissKeyboard() {
        view.endEditing(true)
        if self.view.frame.origin.y != 0 {
            self.view.frame.origin.y = 0
        }
    }
    
    @IBAction func signInBtnTapped(_ sender: Any) {
        
        if usernameTextFld.text != nil && passTextFld.text != nil {
            
            let username = usernameTextFld.text!
            let pass = passTextFld.text!
            
            let data = "PROTOCOLOTFG#" + username + "#" + pass
            outputStream.write(data, maxLength: data.count)
            
            
            var yeyo: NSString!
            
            DispatchQueue.global(qos: .background).async {
                let bufferSize = 1024
                var buffer = Array<UInt8>(repeating: 0, count: bufferSize)

                print("waintig for handshake...")
                
                let bytesRead = self.inputStream.read(&buffer, maxLength: bufferSize)
                if bytesRead >= 0 {
                    var output = NSString(bytes: &buffer, length: bytesRead, encoding: String.Encoding.utf8.rawValue)
                    yeyo = output
                } else {
                    // Handle error
                }
                
//                print("Aqui ta manin -->" + (yeyo as String))
                
            }
            
            
            
            let loggedViewController = storyboard?.instantiateViewController(identifier: Storyboard.loggedViewController) as? LoggedViewController
            
            
            loggedViewController?.setInputStream(inputStream: self.inputStream)
            loggedViewController?.setOutputStream(outputStream: self.outputStream)
            
            view.window?.rootViewController = loggedViewController
            view.window?.makeKeyAndVisible()
        }
        
        
    }
    

}

