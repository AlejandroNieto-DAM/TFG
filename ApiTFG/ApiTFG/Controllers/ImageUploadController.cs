using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace ApiTFG.Controllers
{
   
    [ApiController]
    public class ImageUploadController : ControllerBase
    {
        public static IWebHostEnvironment _environment;

        public ImageUploadController(IWebHostEnvironment environment)
        {
            _environment = environment;
        }

        public class FileUploadApi
        {
            public IFormFile Files { get; set; }
        }

        [HttpPost("SaveImage")]
        public async Task<string> PostFile(FileUploadApi objFile)
        {
            try
            {
                if (objFile.Files.Length > 0)
                {
                    if (!Directory.Exists(_environment.WebRootPath + "\\UPLOAD\\"))
                    {
                        Directory.CreateDirectory(_environment.WebRootPath + "\\UPLOAD\\");
                    }

                    using (FileStream fileStream = System.IO.File.Create(_environment.WebRootPath + "\\UPLOAD\\" + objFile.Files.FileName))
                    {
                        objFile.Files.CopyTo(fileStream);
                        fileStream.Flush();
                        return "\\UPLOAD\\" + objFile.Files.FileName;
                    }

                }
                else
                {
                    return "Failed";
                }


            }
            catch (Exception ex)
            {

                return ex.Message.ToString();
            }
        }

    }
}