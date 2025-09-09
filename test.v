module led_blinker (
    input wire clk_in,     // Connect to BUS_CLK or another clock source
    output wire led        // Connect to P2_1
);

    parameter CLOCK_DIVISOR = 50000000; // Adjust this for 1Hz blinking with 100 MHz clock

    reg [31:0] counter = 0;
    reg led_reg = 0;

    always @(posedge clk_in) begin
        if (counter == (CLOCK_DIVISOR - 1)) begin
            led_reg <= ~led_reg;
            counter <= 0;
        end else begin
            counter <= counter + 1;
        end
    end

    assign led = led_reg;

endmodule

