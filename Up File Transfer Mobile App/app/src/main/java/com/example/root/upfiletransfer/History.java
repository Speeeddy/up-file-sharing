package com.example.root.upfiletransfer;

import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.AsyncTask;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;

import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class History extends AppCompatActivity {

    ListView lv ;
    SwipeRefreshLayout swipeRefreshLayout;
    public String username ;
    public String url = "https://up-karoon.ga/api/um";
    Receive.CustomAdapter fileListAdapter ;
    private String hue = "" ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history);

        swipeRefreshLayout = (SwipeRefreshLayout) findViewById(R.id.swipe2) ;
        swipeRefreshLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                swipeRefreshLayout.setColorSchemeColors(getResources().getColor(R.color.black));
                swipeRefreshLayout.setRefreshing(true);
                Intent i = getIntent() ;
                startActivity(i) ;
                finish() ;
            }
        });
        lv = (ListView) findViewById(R.id.lv2);
        lv.setOnScrollListener(new AbsListView.OnScrollListener()
        {
            @Override
            public void onScrollStateChanged(AbsListView view, int scrollState)
            {

            }

            @Override
            public void onScroll(AbsListView view, int firstVisibleItem, int visibleItemCount, int totalItemCount)
            {
                int topRowVerticalPosition = (lv == null || lv.getChildCount() == 0) ? 0 : lv.getChildAt(0).getTop();
                swipeRefreshLayout.setEnabled(firstVisibleItem == 0 && topRowVerticalPosition >= 0);
            }
        });
        username = getIntent().getStringExtra("username");
        url = url + "/" + username;

        JSONObject jsonObject = new JSONObject() ;
        try {
            jsonObject.put("username" , username) ;
            hue = jsonObject.toString(1) ;
            new JSONTask5().execute();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public class JSONTask5 extends AsyncTask<Void , Void , String > {

        @Override
        protected void onPostExecute(String s) {
            JSONArray parentArray = null;
            try {
                parentArray = new JSONArray(s);
                List<HistoryList> ret = new ArrayList<HistoryList>();
                Gson gson = new Gson();
                for(int i = 0 ; i < parentArray.length() ; i++){
                    JSONArray inner = parentArray.optJSONArray(i) ;
                    Log.d("inner" , inner.toString()) ;
                    HistoryList inn = new HistoryList();
                    inn.setSender(inner.getString(0));
                    Log.d("inner1" , inner.getString(0)) ;
                    inn.setReceiver(inner.getString(1));
                    inn.setFilename(inner.getString(2));
                    Log.d("inner2" , inner.getString(2)) ;

                    inn.setTimestamp(inner.getString(3));
                    inn.setAction(inner.getString(4));
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

                if(ret == null){
                    Toast.makeText(getApplicationContext() , "No File Transfer History!" , Toast.LENGTH_LONG).show();
                    Intent i = new Intent(History.this , SendReceive.class) ;
                    i.putExtra("username" , username) ;
                    startActivity(i) ;
                    finish() ;
                }

                ArrayAdapter adapter = new ArrayAdapter(History.this, android.R.layout.simple_list_item_1
                        , ret){
                    @NonNull
                    @Override
                    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
                        View view = super.getView(position, convertView, parent);
                        TextView tv = (TextView) view.findViewById(android.R.id.text1);
//                        tv.setGravity(Gravity.CENTER);
//                        tv.setTextColor(Color.WHITE);
                        tv.setTypeface(null , Typeface.BOLD);
                        return view ;
                    }
                };
//                fileListAdapter = new Receive.CustomAdapter(R.layout.file_list_item, lists);
                lv.setAdapter(adapter);
            } catch (JSONException e) {
                e.printStackTrace();
            }catch(NullPointerException e){
                e.printStackTrace();
            }
        }

        @Override
        protected String doInBackground(Void... voids) {
            return getServerResponse(hue) ;
        }
    }

    private String getServerResponse(String json){
        HttpPut post  = new HttpPut("https://up-karoon.ga/api/um");
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

    @Override
    public void onBackPressed() {
        Intent i = new Intent(History.this , SendReceive.class) ;
        i.putExtra("username" , username) ;
        startActivity(i) ;
        finish();
    }
}
