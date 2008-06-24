// $(document).ready(function(){
//     $("#bireysel").click(function () {
//         $("#bireysel_kapali").fadeOut("slow");
//         $("#bireysel_acik").fadeIn("slow");
//         $("#bireysel_kapali").attr({ src: "media/img/bireysel_turuncu.png" });
//         $("#bireysel_kapali").animate({
//             src: "media/img/bireysel_turuncu.png"
//         }, 1500 );
//         $("#bireysel").animate({
//             height: 60
//         }, 1500 );
//     });
//
//     $("#bireysel").click(function(){
//         $("#bireysel").animate({
//             backgroundSrc: "media/img/menu/bireysel_turuncu.png";
//         }, 1500 );
//     });
//
//     $("#bireysel").(function () {
//         $("#bireysel_kapali").fadeOut("slow");
//         $("#bireysel_acik").fadeIn("slow");
//         $("#bireysel_kapali").attr({ src: "media/img/bireysel_turuncu.png" });
//         $("#bireysel_kapali").animate({
//             src: "media/img/bireysel_turuncu.png"
//         }, 1500 );
//         $("#bireysel").animate({
//             height: 60
//         }, 1500 );
//     });
// });

// $(document).ready(function(){
//     $("#kurumsal_button").click(function () {
//       $("#kurumsal").slideToggle("slow");
//     });
// 
//     $("#co_button").click(function () {
//       $("#co").slideToggle("slow");
//     });
// 
//     $("#dev_button").click(function () {
//       $("#dev").slideToggle("slow");
//     });
// 
//     $("#bireysel_button").click(function () {
//       $("#bireysel").slideToggle("slow");
//     });
// });

$(document).ready(function(){
    $("#menu").accordion();
});