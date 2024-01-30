module
    DP_ram_dummy
    #(
        parameter WIDTH = 8,
        parameter DEPTH = 1024
    )
    (
        //clk and rst
        input clk,
        //dat interface
        input wr,
        input [$clog2(DEPTH)-1:0] waddr,
        input [WIDTH-1:0] din,
        input rd,
        input [$clog2(DEPTH)-1:0] raddr,
        output reg [WIDTH-1:0] dout
    );

reg [WIDTH-1:0] mem[DEPTH-1:0];

always@(posedge clk) begin
    if(wr) begin
        mem[waddr] <= din;
    end
    else if(rd) begin
        dout <= mem[raddr];
    end
end

endmodule
