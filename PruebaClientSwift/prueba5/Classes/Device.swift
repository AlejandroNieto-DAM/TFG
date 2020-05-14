//
//  Device.swift
//  prueba5
//
//  Created by Alejandro Nieto Alarcon on 12/05/2020.
//  Copyright © 2020 Alejandro Nieto Alarcon. All rights reserved.
//

import Foundation
import UIKit

class Device {
    
    private var id: Int?
    private var identifier_name: String?
    private var state: Int?
    private var maintenance: Int?
    private var image : UIImage!
    
    //Constructor
    init(id: String, identifier_name: String, state: String, maintenance: String) {
        self.id = Int(id)
        self.identifier_name = identifier_name
        self.state = Int(state)
        self.maintenance = Int(maintenance)
    }
    
    //Set the byte[] as the actual image
    public func setImage(image: UIImage){
        self.image = image
    }
    
    //Set the state as the actual state
    public func setState(state: String){
        self.state = Int(state)
    }
    
    //Get the id of the Device
    public func getID() -> Int {
        return self.id!
    }
    
    //Get the identifier_name of the Device
    public func getIdentifierName() -> String {
        return self.identifier_name!
    }
    
    //Get the state of the Device
    public func getState() -> Int {
        return self.state!
    }
    
    //Get the image of the Device
    public func getImage() -> UIImage {
        return self.image!
    }
}
