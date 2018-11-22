package com.example.root.upfiletransfer;

import android.Manifest;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Environment;
import android.os.Handler;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.NotificationCompat;
import android.support.v4.content.FileProvider;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.MimeTypeMap;
import android.widget.AbsListView;
import android.widget.Adapter;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.CheckBox;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;

import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import static android.content.Context.MODE_PRIVATE;

public class Receive extends AppCompatActivity {

    private static final String TAG = "DEBUG";
    ListView lv ;
    public final String url1 = "https://up-karoon.ga/api/fp/";
    public final String url2 = "https://up-karoon.ga/api/ft/";
    public String username ;
    public String filename  ;
    CustomAdapter fileListAdapter ;
    public String cFile ;
    public String cSender ;

    SwipeRefreshLayout swipeRefreshLayout;
    private String hue = "";


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_receive);
        swipeRefreshLayout = (SwipeRefreshLayout) findViewById(R.id.swipe) ;
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
        lv = (ListView) findViewById(R.id.lv);
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
//        Toast.makeText(getApplicationContext(), username , Toast.LENGTH_LONG).show();
        isStoragePermissionGranted();
        String url = url1 + username ;
        new JSONTask().execute(url);

    }



    public class JSONTask extends AsyncTask<String , String , List<ListContent> > {

        @Override
        protected void onPostExecute(final List<ListContent> lists) {
//            while(lists.size() == 0){
//                String url = url1 + username ;
//                new JSONTask().execute(url) ;
//            }
            try {
                ArrayAdapter adapter = new ArrayAdapter(Receive.this, android.R.layout.simple_list_item_1
                        , lists);
                fileListAdapter = new CustomAdapter(R.layout.file_list_item, lists);

                lv.setAdapter(adapter);
                lv.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                    @Override
                    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                        Toast.makeText(getApplicationContext() , "Downloading...Please Wait for Notification." , Toast.LENGTH_LONG).show();
                        ListContent temp = lists.get(position);
                        String sender = temp.getName();
                        filename = temp.getFilename();
                        cFile = filename ;
                        cSender = sender ;
                        String url3 = url2 + username + "/" + sender + "/" + filename;
                        new JSONTask2().execute(url3);
                    }
                });
            }catch(NullPointerException e){
                e.printStackTrace();
            }
        }

        @Override
        protected List<ListContent> doInBackground(String... strings) {
            HttpURLConnection connection = null;
            BufferedReader reader = null;

            try {
                URL url = new URL(strings[0]);
                connection = (HttpURLConnection) url.openConnection();
                connection.connect();
                InputStream stream = connection.getInputStream();
                reader = new BufferedReader(new InputStreamReader(stream));
                StringBuffer buffer = new StringBuffer();
                String line = "";
                while ((line = reader.readLine()) != null) {
                    buffer.append(line);
                }

                String finalJson = buffer.toString();

                Log.d("LAV" , finalJson) ;


//                JSONObject parentObject = new JSONObject(finalJson);
                JSONArray parentArray = new JSONArray(finalJson);
//                Log.d("PARENT" , parentArray.toString()) ;
                List<ListContent> ret = new ArrayList<ListContent>();
                Gson gson = new Gson();


                for(int i = 0 ; i < parentArray.length() ; i++){
                    JSONArray inner = parentArray.optJSONArray(i) ;
                    Log.d("inner" , inner.toString()) ;
                    ListContent inn = new ListContent();
                    inn.setName(inner.getString(0));
                    Log.d("inner1" , inner.getString(0)) ;

                    inn.setFilename(inner.getString(1));
                    Log.d("inner2" , inner.getString(1)) ;

                    inn.setTimestamp(inner.getString(2));
                    inn.setSize(inner.getString(3));
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
//                Collections.sort(ret, new Comparator<ListContent>() {
//
//                    @Override
//                    public int compare(ListContent o1, ListContent o2) {
//                        return (int)(o2.getTimestamp()-o1.getTimestamp());
//                    }
//                });
                return ret ;

            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } catch (JSONException e) {
                e.printStackTrace();
            }
            Log.d("LOL" , " hmm ");
//            Toast.makeText(getApplicationContext(), "LOL!", Toast.LENGTH_LONG).show();

            return null;
        }
    }

    public class JSONTask2 extends AsyncTask<String , String , String> {

        @Override
        protected String doInBackground(String... strings) {
            HttpURLConnection connection = null;
            BufferedReader reader = null;

            try {
                URL url = new URL(strings[0]);
                connection = (HttpURLConnection) url.openConnection();
                connection.connect();
                InputStream stream = connection.getInputStream();
                reader = new BufferedReader(new InputStreamReader(stream));
                StringBuffer buffer = new StringBuffer();
                String line = "";
                while ((line = reader.readLine()) != null) {
                    buffer.append(line);
                }

                String finalJson = buffer.toString();
                byte[] tmp2 = Base64.decode(finalJson, Base64.NO_WRAP);
                String val2 = new String(tmp2, "UTF-8");
                Log.d("VAL", val2);

                FileOutputStream outputStream ;


                String path =
                        Environment.getExternalStorageDirectory() + File.separator  + "UpFileTransfer";
                // Create the folder.
//                File folder = new File(path);
//                folder.mkdirs();

                // Create the file.
                File file = new File(path, filename);
                try
                {
                    FileOutputStream fOut = new FileOutputStream(file);
                    fOut.write(tmp2);
//                    OutputStreamWriter myOutWriter = new OutputStreamWriter(fOut);
//                    myOutWriter.write(val2);
//                    myOutWriter.close();
                    fOut.flush();
                    fOut.close();
                }
                catch (IOException e)
                {
                    Log.e("Exception", "File write failed: " + e.toString());
                }

            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(String s) {
            notificationCall() ;

            JSONObject jsonObject = new JSONObject() ;
            try {
                jsonObject.put("name" , username) ;
                jsonObject.put("sender" , cSender) ;
                jsonObject.put("filename" , cFile) ;
                hue = jsonObject.toString(1) ;

                new AsyncTask<Void , Void , String>(){

                    @Override
                    protected String doInBackground(Void... voids) {
                        return getServerResponse(hue) ;
                    }

                    @Override
                    protected void onPostExecute(String s) {
                        Log.d(s , "Post Download") ;
                    }
                }.execute() ;
            } catch (JSONException e) {
                e.printStackTrace();
            }


        }
    }

    private void notificationCall() {
        Log.d("HELLO" , "CALL" ) ;


//        Intent i = new Intent() ;
//        i.setAction(android.content.Intent.ACTION_VIEW) ;
//        File file = new File(Environment.getExternalStorageDirectory() + File.separator + "/UpFileTransfer/" + filename) ;
//        i.setDataAndType(Uri.fromFile(file), "audio/*");
//        PendingIntent pIntent = PendingIntent.getActivity(this, 0, i, 0);

        Intent i = getOpenFileIntent(Environment.getExternalStorageDirectory() + File.separator + "/UpFileTransfer/" + filename);
        PendingIntent pIntent = PendingIntent.getActivity(this, 0, i, PendingIntent.FLAG_CANCEL_CURRENT);


        NotificationManager mNotificationManager;
        NotificationCompat.Builder mBuilder =
                new NotificationCompat.Builder(this, "notify_001");

//        NotificationCompat.BigTextStyle bigText = new NotificationCompat.BigTextStyle();
//        bigText.bigText(verseurl);
//        bigText.setBigContentTitle("Today's Bible Verse");
//        bigText.setSummaryText("Text in detail");

//        mBuilder.setContentIntent(pendingIntent);
        mBuilder.setSmallIcon(R.mipmap.ic_launcher_round);
        mBuilder.setContentTitle("Download Complete!");
        mBuilder.setContentText("Tap to view " + filename);
        mBuilder.setPriority(Notification.PRIORITY_MAX);
        mBuilder.setSmallIcon(R.drawable.ic_style) ;
        mBuilder.setContentIntent(pIntent);
        mBuilder.setPriority(Notification.PRIORITY_MAX) ;
        mBuilder.setAutoCancel(true) ;

        //        mBuilder.setStyle(bigText);

        mNotificationManager =
                (NotificationManager) this.getSystemService(Context.NOTIFICATION_SERVICE);


        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel("notify_001",
                    "Channel human readable title",
                    NotificationManager.IMPORTANCE_HIGH);
            mNotificationManager.createNotificationChannel(channel);
        }

        mNotificationManager.notify(0, mBuilder.build());
    }

    private Intent getOpenFileIntent(String path) {
        File file = new File(path);
//        Uri uri = Uri.fromFile(file);
        MimeTypeMap mime = MimeTypeMap.getSingleton();
        String extension = fileExt(path);
        String type = mime.getMimeTypeFromExtension(extension);
        Intent intent = new Intent(Intent.ACTION_VIEW);
        intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK);
//        intent.setDataAndType(uri, type);
        Uri apkURI = FileProvider.getUriForFile(
                getApplicationContext(),
                getApplicationContext()
                        .getPackageName() + ".provider", file);
        intent.setDataAndType(apkURI, type);
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        return intent;
    }
    public String fileExt(String filePath){
        int strLength = filePath.lastIndexOf(".");
        if(strLength > 0)
            return filePath.substring(strLength + 1).toLowerCase();
        return null;
    }

    private String getServerResponse(String json){
        HttpDeleteBody post  = new HttpDeleteBody("https://up-karoon.ga/api/ft");
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


    public  boolean isStoragePermissionGranted() {
        if (Build.VERSION.SDK_INT >= 23) {
            if (checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE)
                    == PackageManager.PERMISSION_GRANTED) {
                Log.v(TAG,"Permission is granted");
                return true;
            } else {

                Log.v(TAG,"Permission is revoked");
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
                return false;
            }
        }
        else { //permission is automatically granted on sdk<23 upon installation
            Log.v(TAG,"Permission is granted");
            return true;
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if(grantResults[0]== PackageManager.PERMISSION_GRANTED){
            Log.v(TAG,"Permission: "+permissions[0]+ "was "+grantResults[0]);
            //resume tasks needing this permission
        }
    }

    public class CustomAdapter extends BaseAdapter{

        JSONTask context;
        List<ListContent> files;

        public CustomAdapter(int file_list_item, List<ListContent> lists) {
            this.context = context;
            this.files = lists;
        }

        @Override
        public int getCount() {
            return files.size() ;
        }

        @Override
        public Object getItem(int position) {
            return null;
        }

        @Override
        public long getItemId(int position) {
            return 0;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {

            View v = convertView;

            if (v == null) {
                LayoutInflater inflater = (LayoutInflater)getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                v = inflater.inflate(R.layout.file_list_item, null);
            }

            ListContent file = files.get(position) ;
//            view = getLayoutInflater().inflate(R.layout.mylist,null);

            if (file != null) {
                ImageView imageView = (ImageView)findViewById(R.id.imageView1);
                TextView textView2 = (TextView)findViewById(R.id.textView2) ;
                TextView textView3 = (TextView)findViewById(R.id.textView3) ;

                textView2.setText(file.getFilename());
                textView3.setText(file.getName());

                imageView.setImageResource(R.drawable.ic_style);
                textView2.setText(file.getFilename());
                textView3.setText(file.getName());
            }


            return v;
        }
    }
}