<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            background-color: #efe9e7;
        }

        a {
            text-decoration: none;
            color: #3D1101;
        }

        .wrap {
            max-width: 30rem;
            margin: 20px auto 0 auto;
            height: auto;
        }

        .search {
            position: relative;
            width: 80%;
            float: right;
        }

        .search-bar {
            width: 100%;
            height: 32px;
            font-size: 20px;
            border: 3px solid #3D1101;
            background-color: #efe9e7;
        }

        .search-btn {
            width: 36px;
            height: 32px;
            background-color: #3D1101;
            color: #efe9e7;
            outline: none;
            border: 2px solid #3D1101;
            cursor: pointer;
            position: absolute;
            top: 0;
            right: 0;
        }

        .center {
            display: block;
            margin-left: auto;
            margin-right: auto;

        }
    </style>
</head>

<body style="background-color: rgb(255,248,229)">
    <img src="https://imgur.com/0ltw0Lm.jpg" alt="click icon" width="624" height="445" class="center">
    <div class="wrap">
        <div class="search">
            <input class="search-bar" type="text" placeholder="請輸入機台編號">
            <button class="search-btn" type="button" onclick="javascript:location.href='data_page.html'"><i
                    class="fa fa-fw fa-search"></i></button>
        </div>
    </div>
</body>

</html>