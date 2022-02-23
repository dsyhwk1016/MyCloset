// tradelist

	$(document).ready(function () {
		$.ajax({
			type: "GET",
			url: "/trade/list",
			data: {},
			success: function (response) {
				let rows = response['lists']

				for(let i=0;i < rows.length;i++) {
					let img_path = rows[i]['image_path'];
					let title = rows[i]['title'];
					let status = rows[i]['status'];
					let price = rows[i]['price'];
					let trade_id = rows[i]['_id'];
					let price_s = parseInt(price).toLocaleString()

					let tmp_html = `<div class="col-sm-6 col-md-3">
									<div class="thumbnail">
										<img src="${img_path}" alt="..." style="width:225px; height:260px;">
										<div class="caption">
										<h4>${title}</h4>
										<p class="list_cost"><span class="format-money">${price_s}</span>원</p>
										<p class="list_status">${status}</p>
										<p><a href="/trade/view?goods_id=${trade_id}" class="btn btn-default" role="button">상세보기</a>
										</p>
										</div>
									</div>
								</div>`

					$('#list_card').append(tmp_html);
				}
			}
		})
	})
