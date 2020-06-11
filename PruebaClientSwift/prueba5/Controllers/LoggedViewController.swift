//
//  LoggedViewController.swift
//  prueba5
//
//  Created by Alejandro Nieto Alarcon on 30/03/2020.
//  Copyright © 2020 Alejandro Nieto Alarcon. All rights reserved.
//

import UIKit
import Alamofire

class LoggedViewController: UIViewController, UITableViewDelegate,  UITableViewDataSource  {

    var imagenes = [UIImage]()
    
    private var allDevices = [Device]()

    private let cellSpacingHeight: CGFloat = 15

    private var apiURL = "https://api.unsplash.com/photos/random?" +
                        "client_id=jZIYt--FtgynjvcmEHVcbHEbViKIogcA_KY4wzhE-7Y"
    
    private var clientThread: ClientThread!
    
    @IBOutlet weak var backView: UIView!
    @IBOutlet weak private var tableview: UITableView!
    @IBOutlet weak var image: UIImageView!
    @IBOutlet weak var backButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        loadBackgroundPhoto()
        setUpElements()
        loadDevices()
        setupTableView()
    }
    
    private func setUpElements(){
        backView.backgroundColor = Colors.yellow
        backView.layer.cornerRadius = 50.0
        backView.layer.shouldRasterize = true
        
    }
    
    /**
    * @brief Call to get a random image from one API to load it in the ImageView.
    * @post One image random from api will be loaded into the ImageView
    */
    private func loadBackgroundPhoto(){
        let request = AF.request(apiURL)
        request.responseJSON { (data) in
            //print(data)
            let yeyo = data.description
            
            var first = 0
            var second = 0

            let index = yeyo.range(of: "regular = ")?.lowerBound
            let distance = yeyo.distance(from: yeyo.startIndex, to: index!)
            first = distance + 11
            
            let index2 = yeyo.range(of: "small = ")?.lowerBound
            let distance2 = yeyo.distance(from: index!, to: index2!)
            second = first + distance2
            second = second - 22
            
            //print(yeyo.substring(with: first..<second))
            
            let imageRandom = URL(string: yeyo.substring(with: first..<second))
            
            do {
                let data = try Data(contentsOf: imageRandom!)
                self.image.image = UIImage(data: data)
                //print("Funciona?")
            } catch _ {
                print("Error")
            }
                
        }
    }
    
    private func loadDevices() {
        imagenes.append(UIImage(named: "logo.png")!)
        self.allDevices = self.clientThread.getAllDevices()
    }
    
    public func setClientThread(clientThread: ClientThread){
        self.clientThread = clientThread
    }

    
    private func setupTableView() {
        tableview.delegate = self
        tableview.dataSource = self
    }
    
    internal func numberOfSections(in tableView: UITableView) -> Int {
        return self.allDevices.count
    }
    
    internal func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 1

    }
    
    internal func tableView(_ tableView: UITableView, viewForHeaderInSection section: Int) -> UIView? {
        let headerView = UIView()
        headerView.backgroundColor = UIColor.clear
        return headerView
    }
    
    internal func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 90
    }
    
    // Set the spacing between sections
    internal func tableView(_ tableView: UITableView, heightForHeaderInSection section: Int) -> CGFloat {
        return cellSpacingHeight
    }
    
    internal func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
       
        let cell = Bundle.main.loadNibNamed("DoorEjTableViewCell", owner: self, options: nil)?.first as! DoorEjTableViewCell
        
        self.tableview.backgroundColor = Colors.yellow
        
        cell.heightAnchor.constraint(equalToConstant: 90).isActive = true
        cell.contentView.backgroundColor = Colors.yellow
        cell.viewEsta.layer.cornerRadius = cell.viewEsta.bounds.height / 2
        
        
        if self.allDevices[indexPath.section].getState() == 1 {
            cell.viewEsta.backgroundColor = Colors.open
        } else if self.allDevices[indexPath.section].getState() == 0{
            cell.viewEsta.backgroundColor = UIColor.white
        } else {
            cell.viewEsta.backgroundColor = Colors.firstBlue
        }
                
        //cell.mainImageView.image = self.allDevices[indexPath.section].getImage()
        
        cell.mainImageView.image = self.imagenes[0]
        
        cell.mainImageView.layer.cornerRadius = cell.mainImageView.bounds.height / 2
        cell.mainImageView.backgroundColor = UIColor.gray
        
        cell.mainLabek.text = self.allDevices[indexPath.section].getIdentifierName()
 
        return cell
    }
    
    /**
    * @brief When one device state has changed this method  repaint the TableView.
    * @pre TableView has to load some information previous to call this method.
    * @post TableView will be repainted.
    */
    func refresh(){
        DispatchQueue.main.async { [unowned self] in
            self.tableview.reloadData()
        }
    }
    
    
    // method to run when table view cell is tapped
    internal func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        if self.allDevices[indexPath.section].getState() == 1 {
            self.clientThread.sendCloseDevice(id_device: self.allDevices[indexPath.section].getID())
        } else {
            self.clientThread.sendOpenDevice(id_device: self.allDevices[indexPath.section].getID())
        }
        
        self.tableview.reloadData()
    }
    
    @IBAction private func setFinished(_ sender: Any) {
        self.clientThread.setFinished()
        self.clientThread.sendLogout()
        DispatchQueue.main.async { [unowned self] in
            let viewController = self.storyboard?.instantiateViewController(identifier: Storyboard.viewController) as? ViewController
            
            self.view.window?.rootViewController = viewController
            self.view.window?.makeKeyAndVisible()
        }
    }

}

extension String {
    func index(from: Int) -> Index {
        return self.index(startIndex, offsetBy: from)
    }

    func substring(from: Int) -> String {
        let fromIndex = index(from: from)
        return String(self[fromIndex...])
    }

    func substring(to: Int) -> String {
        let toIndex = index(from: to)
        return String(self[..<toIndex])
    }

    func substring(with r: Range<Int>) -> String {
        let startIndex = index(from: r.lowerBound)
        let endIndex = index(from: r.upperBound)
        return String(self[startIndex..<endIndex])
    }
}

extension ViewController {
    func showNotification(message:String){
        let toastLabel = UILabel(frame: CGRect(x: self.view.frame.width/2-75, y:self.view.frame.height - 100, width: 150, height: 40))
        toastLabel.textAlignment = .center
        toastLabel.alpha = 1.0
        toastLabel.layer.cornerRadius = 10
        toastLabel.backgroundColor = Colors.secondBlue
        toastLabel.textColor = UIColor.white
        toastLabel.clipsToBounds = true
        toastLabel.text = message
        
        self.view.addSubview(toastLabel)
        
        UIView.animate(withDuration: 4.0, delay: 1.0, options: .curveEaseInOut, animations: {
            toastLabel.alpha = 0.0
        }) { (isCompleted ) in
            toastLabel.removeFromSuperview()
        }
    }
}
