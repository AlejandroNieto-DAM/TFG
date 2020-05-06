using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace ApiTFG.Controllers
{
    [ApiController]
    public class ImageController : ControllerBase
    {
    
        [HttpGet("GetImage/{id}")]
        public IActionResult GetImage(String id, String ApiKey)
        {

            try{

                if (ApiKey.Equals("yey"))
                {
                    try
                    {
                        var image = System.IO.File.OpenRead("C:\\Users\\Alejandro\\source\\repos\\ImageApi\\ImageApi\\Images\\" + id + ".jpg");
                        return File(image, "image/png");

                    }
                    catch (FileNotFoundException e)
                    {
                        var image = System.IO.File.OpenRead("C:\\Users\\Alejandro\\source\\repos\\ImageApi\\ImageApi\\Images\\monkeySelfie.jpg");
                        return File(image, "image/png");
                    }

                }

            } 
            catch (NullReferenceException ex)
            {
                
            }

            return null;
        }

        
    }
}