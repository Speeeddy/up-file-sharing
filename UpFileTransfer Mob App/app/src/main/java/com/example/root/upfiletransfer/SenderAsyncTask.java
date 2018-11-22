package com.example.root.upfiletransfer;

import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;
import android.webkit.MimeTypeMap;
import android.widget.Toast;

import org.apache.commons.codec.binary.Base64;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;

public class SenderAsyncTask extends AsyncTask<File , Void , String> {

    private Context context ;
    private String sender ;
    private ProgressDialog dialog;
    private  String receiver ;


    public String hue = "" ;


    public SenderAsyncTask(Context context, String sender, String receiver) {
        this.context = context;
        this.sender = sender;
        this.receiver = receiver;
//        dialog = new ProgressDialog(((SenderActivity) context)) ;
    }


    @Override
    protected void onPreExecute() {
        dialog = ProgressDialog.show( context ,  "",
                "Uploading. Please wait...", true);
    }

    @Override
    protected String doInBackground(File... files) {

        String encode = null ;
        try {
            byte[] bytes = loadFile(files[0]);
            encode = new String(Base64.encodeBase64(bytes));

            Log.d("Encode : ", encode);

//                        encode = "HELLO" ;
            JSONObject jsonObject = new JSONObject();

            jsonObject.put("name", sender);
            jsonObject.put("sendto", receiver);
            jsonObject.put("filename", files[0].getName());
            jsonObject.put("data", encode);
            hue = jsonObject.toString(1);
        } catch (JSONException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return getServerResponse(hue);
    }

    @Override
    protected void onPostExecute(String s) {
//        dialog.dismiss();
//        if(context instanceof  SenderActivity){
//            if(((SenderActivity) context).dialog != null) {
//                ((SenderActivity) context).dialog.dismiss();
//            }
//        }
        if (dialog.isShowing()) {
            dialog.dismiss();
        }
        if (context instanceof SenderActivity) {
            ((SenderActivity) context).bDone.setEnabled(true);
//            ((SenderActivity) context).bCancel.setEnabled(false);
        }
        Toast.makeText(context , s , Toast.LENGTH_LONG).show();
    }

    private String getServerResponse(String json){
        HttpPut post  = new HttpPut("https://up-karoon.ga/api/ft");
        try {
            StringEntity entity = new StringEntity(json);
            post.setEntity(entity);
            Log.d("Entity" , entity.toString()) ;
            post.setHeader("Content-type" , "application/json");
            DefaultHttpClient client = new DefaultHttpClient();
            BasicResponseHandler handler  = new BasicResponseHandler();
            String ret = client.execute(post , handler);
            return ret ;
        } catch (UnsupportedEncodingException e) {
            Log.d("JWP" , e.toString());
        } catch (ClientProtocolException e) {
            Log.d("JWP" , e.toString());
        } catch (IOException e) {
            Log.d("JWP" , e.toString());
        }
        return "UNABLE TO CONTACT SERVER";
    }


    private String getMimeType(String path) {
        String extension = MimeTypeMap.getFileExtensionFromUrl(path);
        return MimeTypeMap.getSingleton().getMimeTypeFromExtension(extension);
    }

    private static byte[] loadFile(File file) throws IOException {
        InputStream is = new FileInputStream(file);

        long length = file.length();
        if (length > Integer.MAX_VALUE) {
            // File is too large
        }
        byte[] bytes = new byte[(int)length];

        int offset = 0;
        int numRead = 0;
        while (offset < bytes.length
                && (numRead=is.read(bytes, offset, bytes.length-offset)) >= 0) {
            offset += numRead;
        }

        if (offset < bytes.length) {
            throw new IOException("Could not completely read file "+file.getName());
        }

        is.close();
        return bytes;
    }
}
