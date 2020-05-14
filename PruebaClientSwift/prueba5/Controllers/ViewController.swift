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
    
    var clientThread: ClientThread!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.clientThread = ClientThread()
        self.setUpElements()
        self.clientThread.setViewController(mainViewController: self)
        clientThread.startConnection() 
    }
    
    private func setUpElements(){
        
        self.hideKeyboardWhenTappedAround()
        NotificationCenter.default.addObserver(self, selector: #selector(keyboardWillShow), name: UIResponder.keyboardWillShowNotification, object: nil)
        
        
        sendBtn.layer.cornerRadius = 25.0
        sendBtn.layer.borderColor = UIColor.black.cgColor
        sendBtn.layer.borderWidth = 2
        
        usernameTextFld.layer.cornerRadius = 25.0
        passTextFld.layer.cornerRadius = 25.0
        
        vmContainer.layer.cornerRadius = 50.0
        vmContainer.layer.shadowColor = UIColor.gray.cgColor
        vmContainer.layer.shadowOffset = .zero
        vmContainer.layer.shadowOpacity = 0.8
        vmContainer.layer.shadowRadius = 50.0
        vmContainer.layer.shadowPath = UIBezierPath(rect: vmContainer.bounds).cgPath
        vmContainer.layer.shouldRasterize = true
        vmContainer.layer.backgroundColor = Colors.yellow.cgColor
        
        vmContainer2.backgroundColor = Colors.gray
        vmContainer2.layer.cornerRadius = 50.0
        vmContainer2.layer.shouldRasterize = true
        
    }
    
    /**
        * @brief
     */
    @objc func keyboardWillShow(notification: NSNotification) {
        if let keyboardSize = (notification.userInfo?[UIResponder.keyboardFrameBeginUserInfoKey] as? NSValue)?.cgRectValue {
            if self.view.frame.origin.y == 0 {
                self.view.frame.origin.y -= keyboardSize.height /  2
            }
        }
    }

    
    /**
     
     */
    func hideKeyboardWhenTappedAround() {
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(dismissKeyboard))
        tap.cancelsTouchesInView = false
        view.addGestureRecognizer(tap)
    }

    /**
     
     */
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
            
            self.clientThread.sendLogin(login: username, password: pass)
            
        }
        
    }
    
    func startsSecondActivity(){

        DispatchQueue.main.async { [unowned self] in
            let loggedViewController = self.storyboard?.instantiateViewController(identifier: Storyboard.loggedViewController) as? LoggedViewController
            
            loggedViewController?.setClientThread(clientThread: self.clientThread)
            
            self.clientThread.setLoggedViewController(loggedViewController: loggedViewController!)
            
            self.view.window?.rootViewController = loggedViewController
            self.view.window?.makeKeyAndVisible()
        }
        
        
    }
    

}

