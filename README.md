# douyuspider   斗魚直播室selenium爬蟲
selenium+模擬滑動動態資料<br/>
思路:<br/>
原本以selenium方式來爬取應該是沒什麼問題<br/>
但是卻遇到滑動加載產生資料的問題,<br/>
以頁面5欄為一列來讀取,利用滑動方式將之定位在每列最後一欄,讓資料產生出來,<br/>
無奈,還是有幾筆資料無法產生,<br/>
因此,將沒有產生出來的資料index記錄下來後,再針對這些資料再一次滑動到該定位來讀取,<br/>
最後終於產生,所以此方法是可行的

