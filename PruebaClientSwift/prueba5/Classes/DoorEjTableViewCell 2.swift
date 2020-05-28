//
//  DoorEjTableViewCell.swift
//  prueba5
//
//  Created by Alejandro Nieto Alarcon on 08/04/2020.
//  Copyright © 2020 Alejandro Nieto Alarcon. All rights reserved.
//

import UIKit

class DoorEjTableViewCell: UITableViewCell {
    
    @IBOutlet weak var mainLabek: UILabel!
    @IBOutlet weak var mainImageView: UIImageView!
    @IBOutlet weak var viewEsta: UIView!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
}
