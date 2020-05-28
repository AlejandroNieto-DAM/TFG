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
    
    private var clientThread: ClientThread!
    
    /**
     *  @brief This method add additional initializations to the view of this controller
     *  @post the variables will be initialized
     */
    override func viewDidLoad() {
        super.viewDidLoad()
        self.clientThread = ClientThread()
        self.setUpElements()
        self.clientThread.setViewController(mainViewController: self)
        clientThread.startConnection() 
    }
    
    
    /**
     *  @brief This method set the styles of some components of the View
     *  @pre The view has to have the components that we are going to style
     *  @post The componentes will change their style for this
     */
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
     *  @brief This method show the keyboard when its needed
     *  @param notification which is the notification of a component that needs the keyboard
     *  @pre One component thats need a keyboard has been tapped
     *  @post The layout will be moved up the keyboard size
     */
    @objc private func keyboardWillShow(notification: NSNotification) {
        if let keyboardSize = (notification.userInfo?[UIResponder.keyboardFrameBeginUserInfoKey] as? NSValue)?.cgRectValue {
            if self.view.frame.origin.y == 0 {
                self.view.frame.origin.y -= keyboardSize.height /  2
            }
        }
    }

    
    /**
     *  @brief Hide de keyboard when the user tap in another side that doesnt need the keyboard
     *  @pre the keyboard has to been active
     *  @post the keyboard will be hide
     */
    private func hideKeyboardWhenTappedAround() {
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(dismissKeyboard))
        tap.cancelsTouchesInView = false
        view.addGestureRecognizer(tap)
    }

    /**
     *  @brief moves the layout to the original position
     *  @pre The user has been tapped in another component that doesnt need the keyboard
     *  @post the layout will go to the original position``
     */
    @objc private func dismissKeyboard() {
        view.endEditing(true)
        if self.view.frame.origin.y != 0 {
            self.view.frame.origin.y = 0
        }
    }
    
    /**
     *  @brief When the button signIn is tapped and the textFields are filled this method will call a thread method to send a msg to the server
     *  @pre the textfields have to be filled
     *  @post a msg will be sent to the server with the login and password
     */
    @IBAction private func signInBtnTapped(_ sender: Any) {
        
        if usernameTextFld.text != nil && passTextFld.text != nil {
            
            let username = usernameTextFld.text!
            let pass = passTextFld.text!
            
            self.clientThread.sendLogin(login: username, password: pass)
            
        }
        
    }
    
    /**
     *  @brief Starts the second activity in the main thread
     *  @pre the login has been successful
     *  @post the sencond activity will start
     */
    public func startsSecondActivity(){

        DispatchQueue.main.async { [unowned self] in
            let loggedViewController = self.storyboard?.instantiateViewController(identifier: Storyboard.loggedViewController) as? LoggedViewController
            
            loggedViewController?.setClientThread(clientThread: self.clientThread)
            self.clientThread.setLoggedViewController(loggedViewController: loggedViewController!)
            
            self.view.window?.rootViewController = loggedViewController
            self.view.window?.makeKeyAndVisible()
        }
        
        
    }
    

}

