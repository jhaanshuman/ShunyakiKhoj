<?//php include('server.php')?>
<!DOCTYPE html>
<html>
<head>
</head>
<body>
    <div id="chatbot">
    <div class="header-chatbot">
        <div id="grieva-exit"><center>X </center></div>
        <img class="grieva" src="./CPGRAMS-Home_files/grieva.jpg">
        <div class="grieva-name"><strong>Ask  GRIEVA </strong></div>

    </div>

    <div id="botcontent">
    	<div id="chatbot-intro">
        	<div class="chatbot-intro-msg">
        	                     <!-- logged in user information -->
         <?php  if (isset($_SESSION['username'])) : ?>
    	 <msg id="msg-username">Hi, <strong><?php echo $_SESSION['username'] ?></strong></msg>
         <?php endif ?>
        	    
		<msg id="msg-bot"><strong>I am Grieva !</strong> Your assistant in resolving grievances with CPGRAMS.</msg>
		</div>
	</div>

        <div id="chatbot-msg-content">

		<div class="chatbot-msg-content-box-header">
			<div id="IssueTag" ><div class="label"> Tag Relevant Issue</div>
			<input type="text" list="Issue" class="list">
			<datalist id="Issue">
			<option issueval="1" value="Administrative Reforms and PG">
			<option issueval="2" value="Agriculture and Cooperation">
			<option issueval="3" value="Agriculture Research and Education">
			<option issueval="4" value="Animal Husbandry, Dairying">
			<option issueval="5" value="Atomic Energy">
			<option issueval="6" value="Ayush">
			<option issueval="7" value="Bio Technology">
			<option issueval="8" value="Central Board of Direct Taxes (Income Tax)">
			<option issueval="9" value="Central Board of Excise and Customs">
			<option issueval="10" value="Chemicals and Petrochemicals">
			<option issueval="11" value="Civil Aviation">
			<option issueval="12" value="Coal">
			<option issueval="13" value="Commerce">
			<option issueval="14" value="Consumer Affairs">
			<option issueval="15" value="Corporate Affairs">
			<option issueval="16" value="Culture">
			<option issueval="17" value="Defence">
			<option issueval="18" value="Defence Finance">
			<option issueval="19" value="Defence Production">
			<option issueval="20" value="Defence Research and Development">
			<option issueval="21" value="Development of North Eastern Region">
			<option issueval="22" value="Drinking Water and Sanitation">
			<option issueval="23" value="Earth Sciences">
			<option issueval="24" value="Economic Affairs">
			<option issueval="25" value="Electronics & Information Technology">
			<option issueval="26" value="Empowerment of Persons with Disabilities">
			<option issueval="27" value="Environment, Forest and Climate Change">
			<option issueval="28" value="Ex Servicemen Welfare">
			<option issueval="29" value="Expenditure">
			<option issueval="30" value="External Affairs">
			<option issueval="31" value="Fertilizers">
			<option issueval="32" value="Financial Services (Banking Division)">
			<option issueval="33" value="Financial Services (Insurance Division)">
			<option issueval="34" value="Financial Services (Pension Reforms)">
			<option issueval="35" value="Fisheries">
			<option issueval="36" value="Food and Public Distribution">
			<option issueval="37" value="Food Processing Industries">
			<option issueval="38" value="Health & Family Welfare">
			<option issueval="39" value="Health Research">
			<option issueval="40" value="Heavy Industry">
			<option issueval="41" value="Higher Education">
			<option issueval="42" value="Home Affairs">
			<option issueval="43" value="Housing and Urban Affairs">
			<option issueval="44" value="Industrial Policy & Promotion">
			<option issueval="45" value="Information and Broadcasting">
			<option issueval="46" value="Investment & Public Asset Management">
			<option issueval="47" value="Justice">
			<option issueval="48" value="Labour and Employment">
			<option issueval="49" value="Land Resources">
			<option issueval="50" value="Legal Affairs">
			<option issueval="51" value="Legislative Department">
			<option issueval="52" value="Micro Small and Medium Enterprises">
			<option issueval="53" value="Mines">
			<option issueval="54" value="Minority Affairs">
			<option issueval="55" value="New and Renewable Energy">
			<option issueval="56" value="NITI Aayog">
			<option issueval="57" value="Comptroller & Auditor General of India">
			<option issueval="58" value="Official Language">
			<option issueval="59" value="Panchayati Raj">
			<option issueval="60" value="Parliamentary Affairs">
			<option issueval="61" value="Pensions and Pensioners Welfare">
			<option issueval="62" value="Personnel and Training">
			<option issueval="63" value="Petroleum and Natural Gas">
			<option issueval="64" value="Pharmaceutical">
			<option issueval="65" value="Posts">
			<option issueval="66" value="Power">
			<option issueval="67" value="Public Enterprises">
			<option issueval="68" value="Railways, ( Railway Board)">
			<option issueval="69" value="Revenue">
			<option issueval="70" value="Road Transport and Highways">
			<option issueval="71" value="Rural Development">
			<option issueval="72" value="School Education and Literacy">
			<option issueval="73" value="Science and Technology">
			<option issueval="74" value="Scientific & Industrial Research">
			<option issueval="75" value="Shipping">
			<option issueval="76" value="Skill Development and Entrepreneurship">
			<option issueval="77" value="Social Justice and Empowerment">
			<option issueval="78" value="Space">
			<option issueval="79" value="Sports">
			<option issueval="80" value="Statistics and Programme Implementation">
			<option issueval="81" value="Steel">
			<option issueval="82" value="Telecommunications">
			<option issueval="83" value="Textiles">
			<option issueval="84" value="Tourism">
			<option issueval="85" value="Tribal Affairs">
			<option issueval="86" value="Unique Identification Authority of India">
			<option issueval="87" value="Water Resources, River Development & Ganga Rejuvenuation">
			<option issueval="88" value="Women and Child Development">
			<option issueval="89" value="Youth Affairs">
			<option issueval="90" value="Other">
			</datalist>
			</div>
		<div id = "container" onload="send_message()">
            <script type="text/javascript">
var username = "  <?php  if (isset($_SESSION['username'])) : ?><strong><?php echo $_SESSION['username'] ?></strong><?php endif ?>, ";
function send_message(init_bot){
var  grieva_init = init_bot;
var prevState;
	var finalTime = new Date();
var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	var year = finalTime.getFullYear();
	var month = finalTime.getMonth()+1 ;
	var monthName = monthNames[finalTime.getMonth()]
	var date = finalTime.getDate();
	var hour = finalTime.getHours()>12 ? finalTime.getHours()-12 : finalTime.getHours();
	var meridian = hour>12 ? "AM" : "PM";
	var minute = finalTime.getMinutes();
	var seconds = finalTime.getSeconds();
	var dateTime = "<br>" +  "<div id='Btime'>" + date + "th " + monthName + " " + year + " " + hour +  ":" + minute + ":" + seconds + " " + meridian + "</div>";

var botname = "<span class='bot_name'>Grieva: </span>";
var botInitText = "<span class='botText'> Hello " + username + " how may i help you ? </span>"
var botInitcontainer = "<div id='bot_container'>" + botInitText + dateTime + "</div>";

    $("#container").html(botInitcontainer);}
	function get_username(init_bot){send_message(" Hello, how may i help you ?");}
	function ai(NewInput){$("#container").html(prevState + NewInput + "<br>");}

$(function(){
	var finalTime = new Date();
var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	var year = finalTime.getFullYear();
	var month = finalTime.getMonth()+1 ;
	var monthName = monthNames[finalTime.getMonth()]
	var date = finalTime.getDate();
	var hour = finalTime.getHours()>12 ? finalTime.getHours()-12 : finalTime.getHours();
	var meridian = hour>12 ? "AM" : "PM";
	var minute = finalTime.getMinutes();
	var seconds = finalTime.getSeconds();
	var UdateTime = "<br>" +  "<div id='Utime'>" + date + "th " + monthName + " " + year + " " + hour + ":" + minute + ":" + seconds + " " + meridian + "</div>";
	var BdateTime = "<br>" +  "<div id='Btime'>" + date + "th " + monthName + " " + year + " " + hour + ":" + minute + ":" + seconds + " " + meridian + "</div>";
    var prevState;
    get_username();

	$("#textbox").keyup(function(event) { if (event.keyCode === 13) {$("#send").click(); } });

      $("#send").click(function(){
        var Input = $("#textbox").val();                        
        var NewInput = Input.toLowerCase().split(" ");
        var InputLen = Input.split(" ").length;
	//var dataBase = database.toLowercase();
	var dbLen = database.length;
	var query = new Array();
	var ans = new Array();
	var k = 0 ;
	var l=0;
	var alt="";

        $("#textbox").val("");
        var prevState = $("#container").html();
        if (prevState.length > 3){prevState = prevState + "";}  

	var userText = "<div class='userText'>" + Input + "</div>";
	var usercontainer = "<br><div id='user_container'>" + userText + UdateTime + "</div>";
	var br = "<br>";

        for(h=0;h<InputLen ;h++){
			for(i=0;i<dbLen;i++){
	   			 for(j=0;j<database[i].split(" ").length;j++){
					var p = NewInput[h];
					var q = database[i].toLowerCase().split(" ")[j];
        				if(p==q){
						alt = alt + " " + p;
						max = alt.split(" ").length
						if(max>k){k=max;}
					for(;l<100;){ans[l] = p; var ind = i; query[l]=i; break;
					}l++;
						b={}; var max='',maxi=0; for(let k of query){if(b[k])b[k]++; else b[k]=1;
						if(maxi<b[k]){max=k;maxi=b[k] }}
   	}    }     }    }
				
		
         
var QbotText = "<div class='botText'>" +"<strong>" + database[max] +"</strong>" + "</div>";
var AbotText = "<div class='botText'>" + answers[max] + " " + "<a href=" + link[max]+ ">" + link[max]+ "</a>"+ "</div>";
var botcontainer = "<div id='bot_container'>" +  QbotText+ "<hr>" + AbotText + BdateTime + "</div>";
	$("#container").html(prevState + usercontainer + br + botcontainer);
       	$("#container").scrollTop($("#container").height()+1500);
        ai(NewInput);
    	});
});
</script>
		 </div>
		</div>
    	</div>
		 <div id="feedbackForm">
			<div class="rating">Rating</div>
			 <div>
			<input id="rateList" type="text" list="Rating">
			<datalist id="Rating">
			<option tagval="1" value="Satisfactory">
			<option tagval="2" value="Good">
			<option tagval="3" value="Unsatisfactory">
			<option tagval="4" value="Not Relevant">
			</datalist>
			</div>
				<div id="fdbkExit" onclick="fdbkexit()"><center>X </center></div>
				<textarea placeholder="Comment Here... (150 Words)" type="text" class="feedbackCmt" max="150"></textarea>
				<button id = "fdbksend">Send</button></div>
	</div>

	<div id="flex-scroller">
	   <script type="text/javascript">     function ShowHideDiv(keyCheck) {
        var ShowKey = document.getElementById("ShowKey"); 
        ShowKey.style.display = keyCheck.checked ? "block" : "none";
	var flex = document.getElementById("flex-scroller")
	flex.style.height = keyCheck.checked ? "70px" : "50px";
	flex.style.top = keyCheck.checked ? "-50px" : "0px";
	var container = document.getElementById("container")
	container.style.height = keyCheck.checked ? "270px" : "320px";
	var content = document.getElementById("botcontent")
	content.style.height = keyCheck.checked ? "365px" : "415px";
    	}</script>
    <div id="keyword"><input for="keyCheck" type="checkbox" class="keyCheck" onclick="ShowHideDiv(this)"><span class="keyword"> Show Sample Questions</span></div><br>
<div id="ShowKey">
	<div id="wrapper"><div class="tube"><div class="subtube" name=""></div></div></div>
	<script type="text/javascript">
	$(function() {

var n=1;
  $(".subtube").html(database[n]);
 
  $(".next").click(function(){ n=n+1;
		 if (n > database.length) {n = 1 ;  $(".subtube").html(database[n]);}
		 else{   $(".subtube").html(database[n]);}; });
  $(".back").click(function(){ n=n-1;
		 if (n < 1) { n = database.length ; $(".subtube").html(database[n]);}
		 else{   $(".subtube").html(database[n]); }; });
})
	    </script>
                    <div id="backnext"><input class="back" value="<" type="button"></div>
                    <div id="backnext"><input class="next" value=">" type="button"></div>
</div>
	</div>
    
    <div class="text-chatbot">
	<div class = "controls">
    
	<textarea id = "textbox" placeholder = "Enter your message here..." autofocus="true" type="text" autocomplete="off" value="Type Your Query Here" maxlength="200"></textarea>
    <button id ="send" name="input_serv">Send</button>
	<script type="text/javascript">
	function feedback(){
		var feedbackForm = document.getElementById("feedbackForm");
		feedbackForm.style.display = "block" ;
	};
	function fdbkexit(){
		var feedbackForm = document.getElementById("feedbackForm");
		feedbackForm.style.display = "none" ;
	};
	</script>
	<div id="feedback">
	<img src="./CPGRAMS-Home_files/Feedback.png" class="feedback" onclick="feedback()"></div>

	</div>
    </div>
</div>
</body>
</html>