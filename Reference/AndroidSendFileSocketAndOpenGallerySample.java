package com.intuitlearning.nsood1.scannerqbui.feature;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;


public class MainActivity extends AppCompatActivity {

    // Currently doesn't fully support image capture, app crashes
    // A previous version used to upload thumbnails of images successfully, but that
    // does not serve the purpose
    // This will need to be fixed

    static final int SELECT_IMAGE = 5;
    // Integer code for gallery image selection, set arbitrarily

    static final int CAPTURE_IMAGE_FULLSIZE_ACTIVITY_REQUEST_CODE = 1777;
    // Integer code for camera image capture, set arbitrarily


    private ImageView mImageView;
    // Display image
    private Button mButtonCamera;
    private Button mButtonGallery;
    private Button mButtonSend;
    private String mCurrentPhotoPath;
    // Photo path required for displaying and uploading, saved after the intent for image selection
    // or capture finishes

    private String IP_UI1 = "qqqq";
    // IP of Server A is hardcoded, can be received from the app also (Not implemented)
    private final int PORT_UI1 = 20000;

    // Click picture intent, app crashes due to some problem in file provider and path
    private void dispatchTakePictureIntent() {
        Intent pictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if(pictureIntent.resolveActivity(getPackageManager()) != null){
            //Create a file to store the image
            File photoFile = null;
            try {
                photoFile = createImageFile();
            } catch (IOException ex) {
                // Error occurred while creating the File
                ex.printStackTrace();
            }
            if (photoFile != null) {
                Uri photoURI = FileProvider.getUriForFile(this,"com.companyname.myname.packagename.fileprovider", photoFile);
                pictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                // Full size image storage
                startActivityForResult(pictureIntent, CAPTURE_IMAGE_FULLSIZE_ACTIVITY_REQUEST_CODE);
            }
        }
    }

    // Creates a new file for saving captured image
    private File createImageFile() throws IOException {
        // Name of file based on the timestamp
        String timeStamp =
                new SimpleDateFormat("yyyyMMdd_HHmmss",
                        Locale.getDefault()).format(new Date());
        String imageFileName = "IMG_" + timeStamp + "_";
        File storageDir =
                getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );

        return image;
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        // On image capture click, request received here after intent to finally process the result
        if (requestCode == CAPTURE_IMAGE_FULLSIZE_ACTIVITY_REQUEST_CODE && resultCode == RESULT_OK) {

            // Decode file in the current photo path
            Bitmap photo = BitmapFactory.decodeFile(mCurrentPhotoPath);
            mImageView.setImageBitmap(photo);
            //ContextWrapper cw = new ContextWrapper(getApplicationContext());

            //File directory = cw.getDir("tmp", Context.MODE_PRIVATE);

            //OutputStream outStream = null;
            //SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            //String filename = "IMG_" + dateFormat.format(new Date()).toString() + ".jpg";

            //File file = new File(mCurrentPhotoPath);
            /*if(!file.exists()) {
                try {
                    file.createNewFile();
                } catch (IOException e) {
                    Log.d("nipun", "onActivityResult: File creation error");
                    e.printStackTrace();
                }
            }*/
            try {
                //outStream = new FileOutputStream(file);
                //photo.compress(Bitmap.CompressFormat.JPEG, 100, outStream);
                //outStream.close();
                Toast.makeText(getApplicationContext(), "Saved", Toast.LENGTH_LONG).show();
                //mCurrentPhotoPath = file.getAbsolutePath();
                Log.d("nipun", "onActivityResult: Filename " + mCurrentPhotoPath);

            } catch (Exception e) {
                e.printStackTrace();
                mCurrentPhotoPath = null;
            }

        }
        // Gallery selected
        else if (requestCode == SELECT_IMAGE)
        {
            if (resultCode == Activity.RESULT_OK)
            {
                Log.d("nipun", "onActivityResult: Opening gallery");
                if (data != null)
                {
                    Uri selectedImageUri = data.getData();
                    Log.d("nipun", "onActivityResult: Some image selected");
                    try {

                        String picturePath = getPath( getApplicationContext( ), selectedImageUri );
                        Log.d("Picture Path", picturePath);
                        mImageView.setImageURI(selectedImageUri);
                        mCurrentPhotoPath = picturePath;
                        // Image path saved
                        Log.d("nipun", "onActivityResult: file path is " + mCurrentPhotoPath);
                    }
                    catch(Exception e) {
                        Log.e("Path Error", e.toString());
                    }

                }
            } else if (resultCode == Activity.RESULT_CANCELED)
            {
                Toast.makeText(getApplicationContext(), "Cancelled", Toast.LENGTH_SHORT).show();
            }
        }
    }

    // Storage permissions required
    public  boolean isStoragePermissionGranted() {
        if (Build.VERSION.SDK_INT >= 23) {
            if (checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE)
                    == PackageManager.PERMISSION_GRANTED) {
                Log.d("storage","Permission is granted");
                return true;
            } else {

                Log.d("storage","Permission is revoked");
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
                return false;
            }
        }
        else { //permission is automatically granted on sdk<23 upon installation
            Log.d("storage","Permission is granted");
            return true;
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if(grantResults[0]== PackageManager.PERMISSION_GRANTED){
            Log.d("storage","Permission: "+permissions[0]+ "was "+grantResults[0]);
            //resume tasks needing this permission
        }
    }

    // Get path of a file from gallery
    public String getPath(Context context, Uri uri ) {
        if (isStoragePermissionGranted()) {
            String result = null;
            String[] proj = {MediaStore.Images.Media.DATA};
            Cursor cursor = context.getContentResolver().query(uri, proj, null, null, null);
            if (cursor != null) {
                if (cursor.moveToFirst()) {
                    int column_index = cursor.getColumnIndexOrThrow(proj[0]);
                    result = cursor.getString(column_index);
                }
                cursor.close();
            }
            if (result == null) {
                result = "Not found";
            }
            return result;
        }
        else
            return null;
    }

    // Launch gallery intent
    private void galleryAddPic() {
        Intent intent = new Intent();
        intent.setType("image/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);//
        startActivityForResult(Intent.createChooser(intent, "Select Picture"), SELECT_IMAGE);
    }

    // Send image to server A
    private boolean CreateSocketAndSend(final String path)
    {
        Log.d("nipun", "CreateSocketAndSend: here");
        // Implemented as a thread so that user is not blocked for the time the image is uploaded

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {

            try {
                //Replace below IP with the IP of that device in which server socket open.
                //If you change port then change the port number in the server side code also.
                Socket socket = new Socket(IP_UI1, PORT_UI1);

                OutputStream outStream = socket.getOutputStream();
                // Output stream
                PrintWriter outPrintWriter = new PrintWriter(outStream);
                // Writer to write text data into the output stream
                BufferedReader inReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                // Reader to read the text from the stream

                Log.d("nipun", "run: buffers created");
                String stringRead = inReader.readLine();
                //go received
                Log.d("nipun", stringRead + " received");

                String filename = path.substring(path.lastIndexOf("/")+1);
                outPrintWriter.print(filename);
                Log.d("nipun", " filename sent " + filename);
                outPrintWriter.flush();
                //filename sent

                stringRead = inReader.readLine();
                //go received
                Log.d("nipun", stringRead + " received");

                File imageFile = new File(path);
                // File read from the filepath provided

                long fileSize = imageFile.length();
                outPrintWriter.print(String.valueOf(fileSize));
                Log.d("nipun", " filesize sent " + String.valueOf(fileSize));
                outPrintWriter.flush();
                // file size sent

                FileInputStream fileStream = null;

                stringRead = inReader.readLine();
                //go received
                Log.d("nipun", stringRead + " received");

                fileStream = new FileInputStream(imageFile);
                byte[] fileBytes = new byte[(int)fileSize];
                fileStream.read(fileBytes);
                //read file in fileBytes

                outStream.write(fileBytes);
                Log.d("nipun", " file sent ");
                outStream.flush();
                //file written using output stream, not printwriter

                stringRead = inReader.readLine();
                //go received
                Log.d("nipun", stringRead + " received");

                // Close all streams
                outPrintWriter.close();
                outStream.close();
                fileStream.close();
                inReader.close();
                socket.close();
            }
            catch (IOException e) {
                e.printStackTrace();
            }

            }
        });

        thread.start();
        try {
            thread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
            Toast.makeText(getApplicationContext(), "Upload failed", Toast.LENGTH_LONG).show();
            return false;
        }
        Toast.makeText(getApplicationContext(), "Successfully uploaded", Toast.LENGTH_LONG).show();
        return true;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mImageView = (ImageView) findViewById(R.id.imageView);
        mButtonCamera = (Button) findViewById(R.id.cameraButton);
        mButtonGallery = (Button) findViewById(R.id.galleryButton);
        mButtonSend = (Button) findViewById(R.id.sendButton);

        // Button click listeners
        mButtonCamera.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                mCurrentPhotoPath = null;
                dispatchTakePictureIntent();
            }
        });

        mButtonGallery.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                mCurrentPhotoPath = null;
                galleryAddPic();
            }
        });

        mButtonSend.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                CreateSocketAndSend(mCurrentPhotoPath);
                mImageView.setImageBitmap(null);
                mCurrentPhotoPath = null;
            }
        });
    }

}
