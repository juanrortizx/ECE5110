function [sol, err] = function_splines(X, Y)
    err = 0;
    n = size(X, 1);

    if n ~= size(Y, 1)
        err = 1;
        error('Matrix dimensions must agree: X is %dx1, Y is %dx1', n, size(Y,1));
    end

    if n < 2
        err = 1;
        error('At least two data points are required.');
    end

    % Number of spline segments
    m = n - 1;

    % Each segment has 4 coefficients: a_i, b_i, c_i, d_i
    % Total unknowns = 4 * (n - 1)
    A = zeros(4 * m, 4 * m);
    B = zeros(4 * m, 1);

    row = 1;

    %% 1) Each spline passes through its left endpoint
    for i = 1:m
        col = 4 * (i - 1) + 1;
        A(row, col)     = X(i)^3;
        A(row, col + 1) = X(i)^2;
        A(row, col + 2) = X(i);
        A(row, col + 3) = 1;
        B(row) = Y(i);
        row = row + 1;
    end

    %% 2) Each spline passes through its right endpoint
    for i = 1:m
        col = 4 * (i - 1) + 1;
        A(row, col)     = X(i + 1)^3;
        A(row, col + 1) = X(i + 1)^2;
        A(row, col + 2) = X(i + 1);
        A(row, col + 3) = 1;
        B(row) = Y(i + 1);
        row = row + 1;
    end

    %% 3) First derivative continuity at interior knots
    for i = 1:m-1
        xk = X(i + 1);

        col1 = 4 * (i - 1) + 1;
        col2 = 4 * i + 1;

        A(row, col1)     =  3 * xk^2;
        A(row, col1 + 1) =  2 * xk;
        A(row, col1 + 2) =  1;

        A(row, col2)     = -3 * xk^2;
        A(row, col2 + 1) = -2 * xk;
        A(row, col2 + 2) = -1;

        B(row) = 0;
        row = row + 1;
    end

    %% 4) Second derivative continuity at interior knots
    for i = 1:m-1
        xk = X(i + 1);

        col1 = 4 * (i - 1) + 1;
        col2 = 4 * i + 1;

        A(row, col1)     =  6 * xk;
        A(row, col1 + 1) =  2;

        A(row, col2)     = -6 * xk;
        A(row, col2 + 1) = -2;

        B(row) = 0;
        row = row + 1;
    end

    %% 5) Natural spline boundary conditions
    % S_1''(X_1) = 0
    A(row, 1) = 6 * X(1);
    A(row, 2) = 2;
    B(row) = 0;
    row = row + 1;

    % S_m''(X_n) = 0
    lastCol = 4 * (m - 1) + 1;
    A(row, lastCol)     = 6 * X(n);
    A(row, lastCol + 1) = 2;
    B(row) = 0;

    %% Solve the linear system
    [sol, err] = function_solve_lsoe(A, B);

end

% function [sol, err] = function_splines(X, Y)
% 
%     err = 0;
%     n = size(X, 1);
% 
%     if n ~= size(Y, 1)
%         error("Matrix dimensions must agree: X is %dx%d and Y is %dx%d", n, size(Y,1));
%     end
% 
%     A = zeros(4*(n-1));
%     B = zeros(4*(n-1), 1);
% 
%     %%Build A and B
% 
%     %Make sure the cubic spline is touching the starting point for each
%     %spline
%     for row = 1:n-1
%         A(row, 4*(row - 1)+1) = X(row)^3;
%         A(row, 4*(row - 1)+2) = X(row)^2;
%         A(row, 4*(row - 1)+3) = X(row);
%         A(row, 4*(row - 1)+4) = 1;
%         B(row, 1) = Y(row);
%     end
% 
%     %Make sure the cubic spline is touching the end point for each spline
%     for row = 1:n-1
%         A(row + n-1, 4*(row - 1)+1) = X(row + 1)^3;
%         A(row + n-1, 4*(row - 1)+2) = X(row + 1)^2;
%         A(row + n-1, 4*(row - 1)+3) = X(row + 1)^1;
%         A(row + n-1, 4*(row - 1)+4) = X(row + 1)^0;
%         B(row + n-1, 1) = Y(row + 1);
%     end
% 
%     %make first dericative of f be equal to 1st derivatie of g
%     for row = 2:n-1
%         A(2*n-2 + row-1, 4*(row-1 - 1) + 1) = 3*X(row)^2;
%         A(2*n-2 + row-1, 4*(row-1 - 1) + 2) = 2*X(row)^1;
%         A(2*n-2 + row-1, 4*(row-1 - 1) + 3) = 1*X(row)^0;
% 
%         A(2*n-2 + row-1, 4*(row-1 - 1) + 4) = 0-3*X(row)^2;
%         A(2*n-2 + row-1, 4*(row-1 - 1) + 5) = 0-2*X(row)^1;
%         A(2*n-2 + row-1, 4*(row-1 - 1) + 6) = 0-1*X(row)^0;
%     end
% 
%     %make second dericative of f be equal to 2nd derivatie of g
%     row = 2*n-2 + (n-1)-1;
%     for ix = 2:n-1
%         row = row + 1;
%         A(row, 4 * (ix - 2) + 1) = 6*X(ix);
%         row = row + 1;
%         A(row, 4 * (ix - 2) + 2) = 2;
%         row = row + 1;
% 
%         A(row, 4 * (ix - 2) + 4) = 0-6*X(ix);
%         row = row + 1;
%         A(row, 4 * (ix - 2) + 5) = 0-2;
%     end
% 
%     %% SOLVE LSOE
%     [sol, err] = function_solve_lsoe(A, B);
% 
%     %% PLOT - SHOW RESULTS
% 
%     for ix= 1:n-1
%         %normalize
%         maxRowFactor = max(abs(A(ix:end,ix:end)'))';
%         A(ix:end,ix:end) =A(ix:end,ix:end)./maxRowFactor;
%         B(ix:end) = B(ix:end) ./ maxRowFactor;
% 
%         %swap rows
%         [~, pivotRow] = max(abs(A(ix:end,ix)));
%         pivotRow = pivotRow + ix -1 ;
%         if pivotRow ~= ix
%             IP = eye(n);
%             lIx = IP(ix,:);
%             lPv = IP(pivotRow,:);
% 
%             IP(ix,:) = lPv;
%             IP(pivotRow,:) = lIx;
%             A = IP*A;
%             B= IP*B;
%         end
% 
%         %reduce
%         M = eye(n);
%         M(ix+1:end,ix) = -A(ix+1:end,ix)/A(ix,ix);
%         A = M*A;
%         B = M*B;
% 
%     end
% 
%     %back sub
%     for ix = n:-1:1
%         sol(ix) = (B(ix)-A(ix,ix+1:n)*sol(ix+1:n))/A(ix,ix);
%     end
% 
% end







% function [sol,err] = function_splines(X , Y)
%     n = size(X, 1);
%     err = 0;
% 
% 
%     if n ~= size(Y,1)
%         err = 1;
%         error('Matrix dimensions must agree: X is %dx%d, Y is %dx1', n, size(Y,1))
%     end
% 
%     A = zeros(4 * (n - 1));
%     B = zeros(4 * (n-1), 1);
% 
%     %% BUILD A and B
%     % make sure the cubic spline is touching the starting point for each spline.
%     for row = 1:n-1
%         A(row, 4 * (row - 1) + 1) = X(row)^3;
%         A(row, 4 * (row - 1) + 2) = X(row)^2;
%         A(row, 4 * (row - 1) + 3) = X(row)^1;
%         A(row, 4 * (row - 1) + 4) = X(row)^0;
%         B(row,1) = Y(row);
%     end
% 
%     % make sure the cubic spline is touching the end point for the spline.
%     for row = 1:n-1
%         A(row + n-1, 4 * (row - 1) + 1) = X(row + 1)^3;
%         A(row + n-1, 4 * (row - 1) + 2) = X(row + 1)^2;
%         A(row + n-1, 4 * (row - 1) + 3) = X(row + 1)^1;
%         A(row + n-1, 4 * (row - 1) + 4) = X(row + 1)^0;
%         B(row + n - 1,1) = Y(row + 1);
%     end
% 
%     % make first derivative of f be equal to 1st derivative of g
%     for row = 2:n-1
%         A(2 * n - 2 + row - 1, 4 *(row - 1 - 1) + 1) = 3 * ( X(row)^2);
%         A(2 * n - 2 + row - 1, 4 *(row - 1 - 1) + 2) = 2 * ( X(row));
%         A(2 * n - 2 + row - 1, 4 *(row - 1 - 1) + 3) = 1;
% 
%         A(2 * n - 2 + row - 1, 4 *(row - 1 - 1) + 1 + 4) = 3 * ( X(row)^2);
%         A(2 * n - 2 + row - 1, 4 *(row - 1 - 1) + 2 + 4) = 2 * ( X(row));
%         A(2 * n - 2 + row - 1, 4 *(row - 1 - 1) + 3 + 4) = 1;
% 
%     end 
%     row = 2 * n - 2 + (n - 1) - 1;
%     for ix = 2:n-1
%         row = row + 1;
%         A(row, 4 * (ix - 2) + 1) = 6 * X(ix);
%         row = row + 1;
%         A(row, 4 * (ix - 2) + 1) = 2;
%         row = row + 1;
% 
%         A(row, 4 * (ix - 2) + 1 + 4) = 0 - 6 * X(ix);
%         row = row + 1;
%         A(row, 4 * (ix - 2) + 1 + 4) = 0 - 2;
%     end
% 
% 
%     %% SOLVE LSOE
%     [sol, err] = function_solve_lsoe(A, B);
% 
%     %% PLOT - SHOW RESULTS
% 
%     for ix= 1:n-1
%         %normalize
%         maxRowFactor = max(abs(A(ix:end,ix:end)'))';
%         A(ix:end,ix:end) =A(ix:end,ix:end)./maxRowFactor;
%         B(ix:end) = B(ix:end) ./ maxRowFactor;
% 
%         %swap rows
%         [~, pivotRow] = max(abs(A(ix:end,ix)));
%         pivotRow = pivotRow + ix -1 ;
%         if pivotRow ~= ix
%             IP = eye(n);
%             lIx = IP(ix,:);
%             lPv = IP(pivotRow,:);
% 
%             IP(ix,:) = lPv;
%             IP(pivotRow,:) = lIx;
%             A = IP*A;
%             B= IP*B;
%         end
% 
%         %reduce
%         M = eye(n);
%         M(ix+1:end,ix) = -A(ix+1:end,ix)/A(ix,ix);
%         A = M*A;
%         B = M*B;
% 
%     end
% 
%     %back sub
%     for ix = n:-1:1
%         sol(ix) = (B(ix)-A(ix,ix+1:n)*sol(ix+1:n))/A(ix,ix);
%     end
% 
% end
% 
% 
