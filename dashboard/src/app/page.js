"use client"
import Image from "next/image";
import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";

const fileTypes = ["JPG", "PNG", "GIF"];

export default function Home() {
  const [file, setFile] = useState(null);
    const handleChange = (uploadedFile) => {
        setFile(URL.createObjectURL(uploadedFile));
    };
  return (
    <div className="flex flex-col gap-10 items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1 className="font-bold text-3xl tracking-[-.05em]">
        Insert your file below
      </h1>
      <p className="font-semibold text-xl tracking-[-.05em] w-[700px] text-center">
        Drag and drop your file containing the prospect detials in the area below. File type supported : csv excel files
      </p>

      <div className="flex flex-col items-center gap-5 border-dashed border-2 border-sky-500 w-[500px] h-[250px] p-[16px] rounded-md flex justify-center">
        <p className="font-bold text-lg tracking-[-.05em]">Drag n drop the files</p>

        <div>
            <FileUploader 
                handleChange={handleChange} 
                name="file" 
                types={fileTypes} />
            {file && (
                <div style={{ marginTop: "20px" }}>
                    <h4>Image Preview:</h4>
                    <img 
                        src={file} 
                        alt="Uploaded Preview" 
                        style={{ maxWidth: "100%", height: "auto" }} />
                </div>
            )}
        </div>
      </div>
    </div>
  );
}
