"use client";
import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";

const fileTypes = ["CSV"];

export default function Home() {
  const [fileData, setFileData] = useState(null);

  const handleChange = (uploadedFile) => {
    if (uploadedFile) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const text = event.target.result;
        setFileData(parseCSV(text));
      };
      reader.readAsText(uploadedFile);
    }
  };

  const parseCSV = (text) => {
    const rows = text.split("\n").map(row => row.split(",")); // Splitting CSV rows and columns
    return rows;
  };

  return (
    <div className="flex flex-col gap-6 relative top-20 items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <h1 className="font-bold text-3xl tracking-[-.05em]">
        Reachify : Automated Client Outreach [Beta testing]
      </h1>
      <p className="font-semibold text-xl tracking-[-.05em] w-[700px] text-center">
        Drag and drop your file containing the prospect details below. File type supported: .csv
      </p>

      <div className="flex flex-col items-center gap-5 border-dashed border-8 border-sky-500 w-[500px] h-[250px] p-[16px] rounded-md">
        <p className="font-bold text-2xl tracking-[-.05em]">Drag & Drop CSV File</p>
        <FileUploader handleChange={handleChange} name="file" types={fileTypes} />
      </div>

      {fileData && (
        <div className="w-[700px] mt-6">
          <h2 className="font-bold text-2xl mb-4">CSV Data:</h2>
          <table className="border-collapse border border-gray-400 w-full">
            <tbody>
              {fileData.map((row, rowIndex) => (
                <tr key={rowIndex} className="border border-gray-300">
                  {row.map((cell, cellIndex) => (
                    <td key={cellIndex} className="border border-gray-300 p-2">{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
