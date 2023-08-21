function [res] = PSDAnalysis(signal, taper1, taper2, fs)
%%
% PSDAnalysis.m analyzes an lfp signal
% Inputs:
%   path: file path to be uploaded for analysis
%   taper1: tapper1 - bandwith
%   taper2: tapper2 - mean time
%   fs: sampling frequency
%   idx_frequency: frequency of the signal to be analyzed
%   range1: initial time to analyze
%   range2: final time to analyze
%
% Ouputs:
%   psd: processed signal
%   f: output frequency
    res = 0;
    try
        params = struct();
        params.tapers = [taper1 taper2];
        params.Fs = fs;

        % calculate pds to first frequency
        [psd, f] = mtspectrumc(signal, params);

        % write data
        data.psd = psd;
        data.f = f;
        % Convierte la estructura de datos en formato JSON
        jsonString = jsonencode(data);

        % Especifica la ruta y el nombre de archivo para guardar el JSON
        nombreArchivo = 'Data/psd_analisys.json';

        % Abre el archivo en modo de escritura
        fid = fopen(nombreArchivo, 'w');

        % Escribe el JSON en el archivo
        fprintf(fid, jsonString);

        % Cierra el archivo
        fclose(fid);

        res = 1;
    catch ME, ME.stack
        disp("ERRROR: error meanwhile read file: " + path);
        disp(ME.identifier);
        disp(ME.message);
    end