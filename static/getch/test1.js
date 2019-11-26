const exchangeRate = 0.91;

// 안 내보냄
function roundTwoDecimals(amount) {
  return Math.round(amount * 100) / 100;
}

// // 내보내기 1
// export function canadianToUs(canadian) {
//   return roundTwoDecimals(canadian * exchangeRate);
// }
//
// // 내보내기 2
// const usToCanadian = function(us) {
//   return roundTwoDecimals(us / exchangeRate);
// };
// export { usToCanadian };

// export default {
//   canadianToUS(canadian) {
//     return roundTwoDecimals(canadian * exchangeRate);
//   },
//
//   usToCanadian: function(us) {
//     return roundTwoDecimals(us / exchangeRate);
//   },
// }


export class Test {
  run() {
    return 1234;
  }
}
