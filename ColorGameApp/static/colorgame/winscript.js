let contractmoney = 12;
let finalcontractmoney = 12;
let contractcount = 1;
let contractselectbtn = '0';
let joinednumber = 0;
var confirmedcontract = {};
let current_tabbar='A';
var curenthour;
var curentminutes;
var curentseconds;
var currentacctbalance=$('.balanceamt').text();
var cab=currentacctbalance;
let getlocalstoragetTabName = localStorage.getItem("tabName");
let hello;
// let otpcount = 0;
$(document).ready(function () {
	function hideLoader()
        {
            $('.loader').hide();
        }
        setTimeout(hideLoader, 1000);
	// add default selected tab
	if(getlocalstoragetTabName!=null){
		tabname = getlocalstoragetTabName[0]
		current_tabbar = tabname[0]
		$('.tab').removeClass('tabselected');
		$('.'+tabname+'tab').addClass('tabselected');
		$('.main_play').removeClass('tabshow');
		$('.' + tabname).addClass('tabshow');
	}
	// end 
	$('.DigitsOnly').keyup(function(){
		this.value = this.value.replace(/[^\d]/g,'');
	})
	$('.DigitsOnly').keydown(function(){
		this.value = this.value.replace(/[^\d]/g,'');
	})
	$('.AlphaOnly').keyup(function(){
		this.value = this.value.replace(/[^a-zA-Z \.]/g,'');
	})
	$('.AlphaOnly').keydown(function(){
		this.value = this.value.replace(/[^a-zA-Z \.]/g,'');
	})
	$('.AlphaNumericOnly').keyup(function(){
		this.value = this.value.replace(/[^0-9a-zA-Z \.]/g,'');
	})
	$('.AlphaNumericOnly').keydown(function(){
		this.value = this.value.replace(/[^0-9a-zA-Z \.]/g,'');
	})
	// [a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}
	$('.number_button').on('click', function () {
		$('input[name="joinnumber"]').val($(this).val());
		$('input[name="joingroup"]').val(current_tabbar);
		joinednumber = $(this).val();
		$('#joinpopup').addClass('popvis');
		$('#ctbtn1').addClass('ct_box_selected');
		$('#ctbtn1').attr('name','contractmoney')
		$('input[name="totalcontractmoney"]').val(contractmoney);
		$('input[name="contractcount"]').val(contractcount);
	});
	$('.cancel').on('click', function () {
		fnClear();
	});
	$('.confirm').on('click', function () {
		// 100 is lesser than 120 ?
		if (parseInt($('.balanceamt').text())<parseInt(finalcontractmoney)){
			alert('insufficient Balance !');
		}else{
		confirmedcontract[joinednumber] =parseInt(finalcontractmoney);
	    }
		fnClear();
	});
	$('.plus').on('click', function () {
		if (contractcount >= 10) {
			return contractcount
		} else {
			contractcount += 1;
			$('#contractcount').html(contractcount);
			$('input[name="contractcount"]').val(contractcount);
			finalcontractmoney = contractmoney * contractcount;
			$('input[name="totalcontractmoney"]').val(finalcontractmoney);
		}
	});
	$('.minus').on('click', function () {
		if (contractcount <= 1) {
			return contractcount
		} else {
			contractcount -= 1;
			$('#contractcount').html(contractcount);
			$('input[name="contractcount"]').val(contractcount);
			finalcontractmoney = contractmoney * contractcount;
			$('input[name="totalcontractmoney"]').val(finalcontractmoney);			
		}
	});
	$('.ctbtn').on('click', function () {
		contractmoney = parseInt($(this).val());
		finalcontractmoney = contractmoney * contractcount
		$('input[name="totalcontractmoney"]').val(finalcontractmoney);
		$('.ctbtn').removeClass('ct_box_selected');
		$('.ctbtn').attr('name','')
		$(this).addClass('ct_box_selected');
		$(this).attr('name','contractmoney')
	});
	function fnClear() {
		$('#joinpopup').removeClass('popvis')
		$('.ctbtn').removeClass('ct_box_selected');
		contractmoney = 12;
		contractcount = 1;
		finalcontractmoney = 12;
	}
	// tabbar query
	$('.tab').on('click', function () {
		$('.tab').removeClass('tabselected');
		$(this).addClass('tabselected');
		let tabbar = $(this).text();
		localStorage.setItem("tabName", $(this).text());
		current_tabbar = tabbar[0];
		$('.main_play').removeClass('tabshow');
		$('.' + current_tabbar).addClass('tabshow');
	});
	
	setInterval(nowDate,1000);
	function nowDate() {
		let d = new Date();
		let sec = d.getSeconds();
		let month = d.getMonth()+1;
		$('.realtime').html(d.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true }));
		$('.realdate').html(d.getDate()+"-"+month+"-"+d.getFullYear())
		// $('.countdownforgame').html(sec);
	}	
	// create Period
		// function countdown(){
		// let dt = new Date();
		// let m = dt.getMinutes();
		// let s = dt.getSeconds();
		// m = s ? 2 - (m % 3) : 3 - (m % 3);
		// if (s) {
		// 	s = 60 - s;
		// }
		// if (s<10){
		// 	s='0'+s;
		// }
		// $('#periodcountdown').html(m+":"+s);
		// if(parseInt(m)==15 && parseInt(s)==00){
		// 	location.reload();
		// }
		// if (parseInt(m)<1){
		// 	$('.winpage').addClass('noselect')
		// 	return false
		// }
		// else{
		// 	$('.winpage').removeClass('noselect')
		// 	return true
		// }
		// //   timer.innerHTML = `${m}:${s < 10 ? '0' + s : s} minutes`;
		// };
		// setInterval(countdown, 1000);
		// function period(){
		// 	let d = new Date();
		// 	let hour = d.getHours();
		// 	let min = d.getMinutes();
		// 	let year = d.getFullYear();
		// 	let month = d.getMonth()+1;
		// 	let date = d.getDate();
		// 	let hor = hour * 60;
		// 	let ur =  hor + min;
		// 	let game = ur/3;
		// 	game = parseInt(game+1);
		// 	let gameperiod = game.toString();
		// 	if ([date].length<2){
		// 		date = '0'+date;
		// 	}
		// 	if([month].length<2){
		// 		month='0'+month;
		// 	}
		// 	if(gameperiod.length==1){
		// 		gameperiod="00"+gameperiod;
		// 	}
		// 	if(gameperiod.length==2){
		// 		gameperiod="0"+gameperiod;
		// 	}
		// 	let periodfulldate = `${year}${month}${date}${gameperiod}`;
		// 	// document.getElementById("game").innerHTML = parseInt(game+1);
		// 	$('#currentperiod').html(periodfulldate);
		// }
		// setInterval(period, 1000);
	// end period











	// setTimeout(turnoffgifimage, 2000);
	// function turnoffgifimage(){
	// 	$('.playimage').removeClass('bannerimage');
	// 	$('.playimagegif').addClass('bannerimage');
	// }

    // $('.btnSendOTP').on('click',function(){
	// 	if($("#PhoneNumber").val() != "" && $("#PhoneNumber").val().length == 10)
	// 	{
	// 		$('.btnVerifyOTP').removeClass('disablediv');
	// 		$('.btnSendOTP').addClass('disablediv');
	// 		if (otpcount==0 || otpcount==1){
	// 			otpcount+=1
	// 			setTimeout(resendOTP, 60000);
	// 			Android.SendVerificationCode('+91'+$("#PhoneNumber").val());
	// 		}
	// 		else{
	// 			alert('try again after 24hrs!');
	// 			$('.btnSendOTP').addClass('disablediv');
	// 			$('.btnVerifyOTP').addClass('disablediv');
	// 		}
			
			
	// 		function resendOTP(){
	// 			if (otpcount==0 || otpcount==1){
	// 			$('.btnSendOTP').removeClass('disablediv');
	// 			$('.btnSendOTP').html('Resend OTP')
	// 			$('.btnVerifyOTP').removeClass('disablediv');
	// 			}else{
	// 				$('.btnSendOTP').addClass('disablediv');
	// 			}
	// 		}
	// 	}
	// });

	// $('.btnVerifyOTP').on('click',function(){
	// 	if($("#otp").val() != "" && $("#otp").val().length == 6)
	// 	{
	// 		otpcount=2;
	// 		$('.btnSendOTP').addClass('disablediv');
	// 		$('.btnVerifyOTP').addClass('disablediv');
	// 		Android.verifyOTPCode($("#otp").val());
	// 	}else{
	// 		$('.btnVerifyOTP').removeClass('disablediv');
	// 		alert('check entered OTP!');
	// 	}
	// });


	$('.bankcardbtn').on('click',function(){
		// show addbakdet_card
		$('.addbakdet_card').removeClass('tabhide');

		// hide showbankdetails showbankdetails
		$('.showbankdetails').addClass('tabhide');
		$('.addbank').addClass('tabhide');
		
		
	})
	$('.upiidbtn').on('click',function(){
		// show addbakdet_card
		$('.addupiId').removeClass('tabhide');

		// hide showbankdetails showbankdetails
		$('.showbankdetails').addClass('tabhide');
		$('.addbank').addClass('tabhide');
		
	})
	$('.VerifyUPIID').on('click',function(){
		if($('#upi').val()!=''){
			var upi = $('#upi').val();
			var match = /[a-zA-Z0-9_]{3,}@[a-zA-Z]{3,}/;
			if(match.test(upi)){
				$('#upisubmit').prop('disabled',false);

			}else{
				alert('entered upi is incorrect! please check again')
			}
			

		}else{
			alert('enter upi to verify');
			$('#upisubmit').prop('disabled',true);
		}
	})




});

function goBack() {
	window.history.back();
}

// function isVerified(val){
// 	console.log(val);
// 	if(val)
// 	{
// 		otpcount=2;
// 		$('#txtpassword').prop('disabled',false);
// 		$('#btnRegister').prop('disabled',false);
// 		$('.btnVerifyOTP').addClass('disablediv');
// 		$('.btnSendOTP').addClass('disablediv');
// 	}
// 	else
// 	{
// 		$('.btnVerifyOTP').removeClass('disablediv');
// 		$('#txtpassword').prop('disabled',true);
// 		$('#btnRegister').prop('disabled',true);
// 		alert('Invalid OTP')
// 	}
// }
