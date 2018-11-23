package com.example.root.upfiletransfer;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.CardView;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.UnsupportedEncodingException;

public class DeletePair extends AppCompatActivity {

    EditText tvDeleting ;
    CardView card4;
    String username ;


    private String hue = "";
    private String hue2 = "";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_delete_pair);

        tvDeleting = (EditText) findViewById(R.id.tvDeleting) ;
        card4 = (CardView) findViewById(R.id.card4) ;

        username = getIntent().getStringExtra("username") ;

        card4.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final String user = tvDeleting.getText().toString() ;

                final JSONObject jsonObject = new JSONObject() ;
                try {
                    jsonObject.put("username" , tvDeleting.getText().toString()) ;
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
                                JSONObject jsonObject1 = new JSONObject() ;
                                try{
                                    jsonObject1.put("sender" , tvDeleting.getText().toString()) ;
                                    jsonObject1.put("receiver" , username) ;
                                    hue2 = jsonObject1.toString(1) ;
                                    Log.d("hue2" , hue2) ;
                                    new AsyncTask<Void , Void , String>(){

                                        @Override
                                        protected String doInBackground(Void... voids) {
                                            return getServerResponse1(hue2);
                                        }

                                        @Override
                                        protected void onPostExecute(String s) {
                                            Toast.makeText(getApplicationContext() , s , Toast.LENGTH_LONG).show();
                                            Intent i = new Intent(DeletePair.this , SendReceive.class) ;
                                            i.putExtra("username" , username) ;
                                            startActivity(i) ;
                                            finish() ;
                                        }
                                    }.execute();
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                            }else{
                                Toast.makeText(getApplicationContext() , s , Toast.LENGTH_LONG).show();
                            }
                        }
                    }.execute() ;
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });

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

    private String getServerResponse1(String json){
        HttpPost post  = new HttpPost("https://up-karoon.ga/api/pm/removePairing");
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
        return ret;
    }


}
