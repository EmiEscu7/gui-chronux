function [res] = SpectogramAnalysis(movingwin, tapers, fpass, fs, err, trialave, folder, file_name)
%%
% SpectogramAnalysis.m analyzes an lfp signal   
% Inputs:
%   path: file path to be uploaded for analysis
%   movingwin: analysis window
%   tapers: [taper1 taper2] - bandwith
%   fpass: frequency band to be used in the calculation
%   fs: sampling frequency
%   err: error calculation
%   trialave: average over trials/channels when 1, don't average when 0
%   idx: neuron index
%
% Ouputs:
%   S: processed signal
%   t: time of the process
%   f: output frequency
    res = 0;
    try 
        
        % Specify the path to your JSON file
        jsonFilePath = "Data/Signal/signal.json";

        % Read the JSON file
        jsonData = jsondecode(fileread(jsonFilePath));
        
        signal = eval(jsonData.signal);
        
        % Remove (delete) the JSON file
        delete(jsonFilePath);
        
        params = struct();
        params.tapers = tapers;    
        params.fpass = fpass;
        params.Fs = fs; 
        params.trialave = trialave;
        params.err = err;

        % calculate pds to first frequency
        [S, t, f] = mtspecgramc(signal, movingwin, params);
        
        data.S = S;
        data.t = t;
        data.f = f;

        % Convierte la estructura de datos en formato JSON
        jsonString = jsonencode(data);

        % Especifica la ruta y el nombre de archivo para guardar el JSON
        nombreArchivo = convertCharsToStrings(folder) + convertCharsToStrings(file_name) + ".json";

        % Abre el archivo en modo de escritura
        fid = fopen(nombreArchivo, 'w');

        % Escribe el JSON en el archivo
        fprintf(fid, jsonString);

        % Cierra el archivo
        fclose(fid);

        res = 1;
    catch ME, ME.stack
        disp(ME.identifier);
        disp(ME.message);
    end