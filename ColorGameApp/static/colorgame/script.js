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
let otpcount = 0;
$(document).ready(function () {
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
		alert( current_tabbar+ " " + joinednumber + " ," + "Contract Amount" + " " + finalcontractmoney);
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
		contractmoney = 10;
		contractcount = 1;
		finalcontractmoney = 10;
	}
	// tabbar query
	$('.tab').on('click', function () {
		$('.tab').removeClass('tabselected');
		$(this).addClass('tabselected');
		let tabbar = $(this).text();
		current_tabbar = tabbar[0];
		$('.main_play').removeClass('tabshow');
		$('.' + current_tabbar).addClass('tabshow');
	});
	
	setInterval(nowDate,1000);
	function nowDate() {
		let d = new Date();
		let sec = d.getSeconds();
		$('.realtime').html(d.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true }));
		// $('.countdownforgame').html(sec);
	}	
	// create Period
		function countdown(){
		let dt = new Date();
		let m = dt.getMinutes();
		let s = dt.getSeconds();
		m = s ? 14 - (m % 15) : 15 - (m % 15);
		if (s) {
			s = 60 - s;
		}
		if (s<10){
			s='0'+s;
		}
		$('#periodcountdown').html(m+":"+s);
		//   timer.innerHTML = `${m}:${s < 10 ? '0' + s : s} minutes`;
		};
		setInterval(countdown, 1000);
		function period(){
			let d = new Date();
			let hour = d.getHours();
			let min = d.getMinutes();
			let year = d.getFullYear();
			let month = d.getMonth()+1;
			let date = d.getDate();
			let hor = hour * 60;
			let ur =  hor + min;
			let game = ur/15;
			game = parseInt(game+1);
			let gameperiod = game.toString();
			if ([date].length<2){
				date = '0'+date;
			}
			if([month].length<2){
				month='0'+month;
			}
			console.log( gameperiod.length);
			if(gameperiod.length==1){
				gameperiod="00"+gameperiod;
			}
			if(gameperiod.length==2){
				gameperiod="0"+gameperiod;
			}
			let periodfulldate = `${year}${month}${date}${gameperiod}`;
			// document.getElementById("game").innerHTML = parseInt(game+1);
			$('#currentperiod').html(periodfulldate);
		}
		setInterval(period, 1000);
	// end period











	setTimeout(turnoffgifimage, 2000);
	function turnoffgifimage(){
		$('.playimage').removeClass('bannerimage');
		$('.playimagegif').addClass('bannerimage');
	}

    $('.btnSendOTP').on('click',function(){
		if($("#PhoneNumber").val() != "" && $("#PhoneNumber").val().length == 10)
		{
			$('.btnVerifyOTP').removeClass('disablediv');
			$('.btnSendOTP').addClass('disablediv');
			if (otpcount==0 || otpcount==1){
				otpcount+=1
				setTimeout(resendOTP, 60000);
				Android.SendVerificationCode('+91'+$("#PhoneNumber").val());
			}
			else{
				$('.btnSendOTP').addClass('disablediv');
				$('.btnVerifyOTP').addClass('disablediv');
			}
			
			
			function resendOTP(){
				$('.btnSendOTP').removeClass('disablediv');
				$('.btnSendOTP').html('Resend OTP')
				$('.btnVerifyOTP').removeClass('disablediv');
			}
		}
	});

	$('.btnVerifyOTP').on('click',function(){
		if($("#otp").val() != "" && $("#otp").val().length == 6)
		{
			$('.btnVerifyOTP').addClass('disablediv');
			Android.verifyOTPCode($("#otp").val());
		}
	});
});

function goBack() {
	window.history.back();
}

function isVerified(val){
	console.log(val);
	if(val)
	{
		$('#txtpassword').prop('disabled',false);
		$('#btnRegister').prop('disabled',false);
		$('.btnVerifyOTP').addClass('disablediv');
		$('.btnSendOTP').addClass('disablediv');
	}
	else
	{
		$('#txtpassword').prop('disabled',true);
		$('#btnRegister').prop('disabled',true);
		alert('Invalid OTP')
	}
}
