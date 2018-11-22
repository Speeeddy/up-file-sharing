package com.example.root.upfiletransfer;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.CardView;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.webkit.MimeTypeMap;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;

import org.apache.commons.codec.binary.Base64;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class PeerChooserActivity extends AppCompatActivity {

    EditText tvReceiver;
    TextView bSendFinal;

    ArrayList<File> filesToBeSent ;

    ListView lv ;
    public String username ;

    List<String> temp ;
    public String hue = "" ;
    public String hue2 = "" ;
    CardView card2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_peer_chooser);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {

            getWindow().setFlags(WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
                    WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS);
        }

        lv = (ListView) findViewById(R.id.pairedList) ;
        tvReceiver = (EditText) findViewById(R.id.tvReceiver) ;
        bSendFinal = (TextView) findViewById(R.id.bSendFinal) ;


        filesToBeSent = (ArrayList<File>) getIntent().getSerializableExtra("filesToBeSent");
        username = getIntent().getStringExtra("username");




        JSONObject jsonObject = new JSONObject() ;
        try {
            jsonObject.put("receiver" , username) ;
            hue2 = jsonObject.toString(1) ;
            new JSONTask6().execute();
        } catch (JSONException e) {
            e.printStackTrace();
        }


        card2 = (CardView) findViewById(R.id.card2) ;
        card2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final String user = tvReceiver.getText().toString() ;

                JSONObject jsonObject = new JSONObject() ;
                try {
                    jsonObject.put("username" , tvReceiver.getText().toString()) ;
                    hue = jsonObject.toString(1) ;

                    new AsyncTask<Void , Void , String>(){

                        @Override
                        protected String doInBackground(Void... voids) {
                            return getServerResponse(hue) ;
                        }

                        @Override
                        protected void onPostExecute(String s) {
                            s = s.replaceAll("\\s+","");
                            if(s.trim().toString().equals("\"Userexists\"")){
                                Intent i = new Intent(getApplicationContext() , SenderActivity.class) ;
                                i.putExtra("filesToBeSent" , filesToBeSent) ;
                                i.putExtra("sender" , username) ;
                                i.putExtra("receiver" , user) ;
                                startActivity(i);
                            }else{
                                Toast.makeText(getApplicationContext() , s , Toast.LENGTH_LONG).show();
                            }
                        }
                    }.execute() ;
                } catch (JSONException e) {
                    e.printStackTrace();
                }



//                for(File f : filesToBeSent){
//                    String encode = null ;
//                    try {
//
//                        byte[] bytes = loadFile(f);
//                        encode = new String(Base64.encodeBase64(bytes));
//
//                        Log.d("Encode : " , encode) ;
//
////                        encode = "HELLO" ;
//                        JSONObject jsonObject = new JSONObject() ;
//
//                        jsonObject.put("name" , username);
//                        jsonObject.put("sendto" , user);
//                        jsonObject.put("filename" , f.getName());
//                        jsonObject.put("data" , encode) ;
//                        hue = jsonObject.toString(1) ;
//
//                        Log.d("HUE" , hue) ;
//
//                        new AsyncTask<Void,Void,String>(){
//
//                        @Override
//                        protected String doInBackground(Void... voids) {
//                            return getServerResponse(hue);
//                        }
//
//                        @Override
//                        protected void onPostExecute(String s) {
//                            Toast.makeText(getApplicationContext() , s , Toast.LENGTH_LONG).show();
//                        }
//                    }.execute();
//
//                    } catch (FileNotFoundException e) {
//                        e.printStackTrace();
//                    } catch (IOException e) {
//                        e.printStackTrace();
//                    } catch (JSONException e) {
//                        e.printStackTrace();
//                    }
//                }
            }
        });

//        bSendFinal.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                String user = tvReceiver.getText().toString() ;
//
//
//                Intent i = new Intent(getApplicationContext() , SenderActivity.class) ;
//                i.putExtra("filesToBeSent" , filesToBeSent) ;
//                i.putExtra("sender" , username) ;
//                i.putExtra("receiver" , user) ;
//                startActivity(i);
//
////                for(File f : filesToBeSent){
////                    String encode = null ;
////                    try {
////
////                        byte[] bytes = loadFile(f);
////                        encode = new String(Base64.encodeBase64(bytes));
////
////                        Log.d("Encode : " , encode) ;
////
//////                        encode = "HELLO" ;
////                        JSONObject jsonObject = new JSONObject() ;
////
////                        jsonObject.put("name" , username);
////                        jsonObject.put("sendto" , user);
////                        jsonObject.put("filename" , f.getName());
////                        jsonObject.put("data" , encode) ;
////                        hue = jsonObject.toString(1) ;
////
////                        Log.d("HUE" , hue) ;
////
////                        new AsyncTask<Void,Void,String>(){
////
////                        @Override
////                        protected String doInBackground(Void... voids) {
////                            return getServerResponse(hue);
////                        }
////
////                        @Override
////                        protected void onPostExecute(String s) {
////                            Toast.makeText(getApplicationContext() , s , Toast.LENGTH_LONG).show();
////                        }
////                    }.execute();
////
////                    } catch (FileNotFoundException e) {
////                        e.printStackTrace();
////                    } catch (IOException e) {
////                        e.printStackTrace();
////                    } catch (JSONException e) {
////                        e.printStackTrace();
////                    }
////                }
//            }
//        });

    }

    private String getServerResponse(String json){
        HttpPost post  = new HttpPost("https://up-karoon.ga/api/um/check");
        String ret = "UNABLE TO CONTACT SERVER" ;
        HttpResponse httpResponse ;
        try {
            StringEntity entity = new StringEntity(json);
            post.setEntity(entity);
            Log.d("Entity" , entity.toString()) ;
            post.setHeader("Content-type" , "application/json");
            DefaultHttpClient client = new DefaultHttpClient();
            httpResponse = client.execute(post) ;
//            ret = client.execute(post , handler);
            ret = EntityUtils.toString(httpResponse.getEntity()) ;
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

    public class JSONTask6 extends AsyncTask<Void , Void , String>{

        @Override
        protected void onPostExecute(String s) {
            JSONArray parentArray = null;
            try {
                parentArray = new JSONArray(s);
                final List<String> ret = new ArrayList<String>();
                Gson gson = new Gson();
                for(int i = 0 ; i < parentArray.length() ; i++){
                    JSONArray inner = parentArray.optJSONArray(i) ;
                    Log.d("inner" , inner.toString()) ;
                    String inn ;
                    inn = inner.getString(0);
                    Log.d("inner1" , inner.getString(0)) ;
                    ret.add(inn) ;
//                    JSONArray o = null;
//                    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
//                        o = new JSONArray(parentArray.getJSONArray(i));
//                        Log.d("OO" , o.toString(1));
//                    }
////                    ListContent inn = gson.fromJson( o.toString() , ListContent.class) ;
//                    ListContent inn = new ListContent();
//                    inn.setName(o.getString(0));
//                    inn.setFilename(o.getString(1));
//                    ret.add(inn) ;
//                    Log.d("HELLO" , inn.getFilename()) ;
                }
                ArrayAdapter adapter = new ArrayAdapter(PeerChooserActivity.this, android.R.layout.simple_list_item_1
                        , ret);
//                fileListAdapter = new Receive.CustomAdapter(R.layout.file_list_item, lists);
                lv.setAdapter(adapter);
                lv.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                    @Override
                    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                        try{
                            String add = ret.get(position) ;
                            Log.d("TRYIED" , "LOL") ;
                            String first = tvReceiver.getText().toString() ;
                            String second ;
                            if(first.length() == 0){
                                second = add ;
                            }else{
                                second = first + "," + add;
                            }
                            tvReceiver.setText(second);
                            tvReceiver.setSelection(tvReceiver.getText().length());
                        }catch (NullPointerException e){
                            e.printStackTrace();
                        }
                    }
                });
            } catch (JSONException e) {
                e.printStackTrace();
            }catch(NullPointerException e){
                e.printStackTrace();
            }
        }

        @Override
        protected String doInBackground(Void... voids) {
            return getServerResponse2(hue2) ;
        }
    }

    private String getServerResponse2(String json){
        HttpPost post  = new HttpPost("https://up-karoon.ga/api/pm/getPairs");
        String ret = "UNABLE TO CONTACT SERVER" ;
        HttpResponse httpResponse ;
        try {
            StringEntity entity = new StringEntity(json);
            post.setEntity(entity);
            Log.d("Entity" , entity.toString()) ;
            post.setHeader("Content-type" , "application/json");
            DefaultHttpClient client = new DefaultHttpClient();
            httpResponse = client.execute(post) ;
//            ret = client.execute(post , handler);
            ret = EntityUtils.toString(httpResponse.getEntity()) ;
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
