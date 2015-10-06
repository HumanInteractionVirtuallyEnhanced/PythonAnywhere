<?php
    $apiKey         = '55977b64122d41058d1edaf8326d0ff9-us4'; // Input your Mailchimp API Key
    $listId         = 'e83a30cc73'; // Input your List ID
    $double_optin   = false;
    $send_welcome   = false;
    $email_type     = 'html';
    $email          = $_POST['email'];
    $name           = $_POST['name'];

    //replace us4 with your actual datacenter
    $submit_url     = "http://us4.api.mailchimp.com/1.3/?method=listSubscribe";

    $data = array(
        'email_address' => $email,
        'apikey'        => $apiKey,
        'id'            => $listId,
        'double_optin'  => $double_optin,
        'send_welcome'  => $send_welcome,
        'email_type'    => $email_type,
        'merge_vars'    => array(
            'FNAME'     => $name
        )
    );

    $payload = json_encode($data);
     
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $submit_url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, urlencode($payload));
     
    $result = curl_exec($ch);
    curl_close ($ch);

    $data = json_decode($result);

    if ($data->error){
        echo $data->error;
    } else {
        echo "Got it, you've been added to our email list.";
    }