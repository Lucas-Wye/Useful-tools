`define SCR1_DMEM_DWIDTH 32

module Montgomery (
	input logic clk,
	input logic rst_n,

	input logic[`SCR1_DMEM_DWIDTH-1:0] q,
	input logic[`SCR1_DMEM_DWIDTH-1:0] q_Prime,

	input logic[`SCR1_DMEM_DWIDTH-1:0] data_in_1,
	input logic[`SCR1_DMEM_DWIDTH-1:0] data_in_2,

	output logic[`SCR1_DMEM_DWIDTH-1:0] data_out
);
// Note that R is selected as 2 ^ (`SCR1_DMEM_DWIDTH).

// stage 1: T = a * b
logic[2 * `SCR1_DMEM_DWIDTH-1:0] T;
logic[2 * `SCR1_DMEM_DWIDTH-1:0] T_stage_1;
assign T = data_in_1 * data_in_2;
always @ (posedge clk) begin
	T_stage_1 <= T;
end

// stage 2: m = T * q' % R
logic[`SCR1_DMEM_DWIDTH-1:0] m;
logic[2 * `SCR1_DMEM_DWIDTH-1:0] T_stage_2;
logic[`SCR1_DMEM_DWIDTH-1:0] m_stage_2;
assign m = T_stage_1 * q_Prime;
always @ (posedge clk) begin
	T_stage_2 <= T_stage_1;
	m_stage_2 <= m;
end

// stage 3: k = q * m
logic[2 * `SCR1_DMEM_DWIDTH-1:0] k;
logic[`SCR1_DMEM_DWIDTH-1:0] T_stage_3;
logic[2 * `SCR1_DMEM_DWIDTH-1:0] k_stage_3;
assign k = q * m_stage_2;
always @ (posedge clk) begin
	T_stage_3 <= T_stage_2;
	k_stage_3 <= k;
end

// stage 4: t = (T + k) / R
logic[`SCR1_DMEM_DWIDTH-1:0] t;
logic[`SCR1_DMEM_DWIDTH-1:0] t_stage_4;
assign t = (T_stage_3 + k_stage_3) >> `SCR1_DMEM_DWIDTH;
always @ (posedge clk) begin
	t_stage_4 <= t;
end

// stage 5: output
logic[`SCR1_DMEM_DWIDTH-1:0] t_minus_q;
logic[`SCR1_DMEM_DWIDTH-1:0] mont_out;
assign t_minus_q = t_stage_4 - q;
always @ (posedge clk) begin
	if(t_stage_4 > q) begin
		mont_out <= t_minus_q;
	end else begin
		mont_out <= t_stage_4;
	end
end

assign data_out = mont_out;

endmodule: Montgomery