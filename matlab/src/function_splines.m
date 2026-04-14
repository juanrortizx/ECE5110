function [sol,err] = function_splines(X , Y)
    n = size(X, 1);
    err = 0;


    if n ~= size(Y,1)
        err = 1;
        error('Matrix dimensions must agree: X is %dx%d, Y is %dx1', n, size(Y,1))
    end
    
    A = zeros(4 * (n - 1));
    B = zeros(4 * (n-1), 1);

    %% BUILD A and B
    % make sure the cubic spline is touching the starting point for each spline.
    for row = 1:n-1
        A(row, 4 * (row - 1) + 1) = X(row)^3;
        A(row, 4 * (row - 1) + 2) = X(row)^2;
        A(row, 4 * (row - 1) + 3) = X(row)^1;
        A(row, 4 * (row - 1) + 4) = X(row)^0;
        B(row,1) = Y(row);
    end

    % make sure the cubic spline is touching the end point for the spline.
    for row = 1:n-1
        A(row + n-1, 4 * (row - 1) + 1) = X(row + 1)^3;
        A(row + n-1, 4 * (row - 1) + 2) = X(row + 1)^2;
        A(row + n-1, 4 * (row - 1) + 3) = X(row + 1)^1;
        A(row + n-1, 4 * (row - 1) + 4) = X(row + 1)^0;
        B(row + n - 1,1) = Y(row + 1);
    end

    % make first derivative of f be equal to 1st derivative of g
    for row = 2:n-1
        A(2 * n - 2 + row - 1, 4 *(row - 1 - 1) + 1) = 3 * ( X(row)^2);
        A(2 * n - 2 + row - 1, 4 *(row - 1 - 1) + 2) = 2 * ( X(row));
        A(2 * n - 2 + row - 1, 4 *(row - 1 - 1) + 3) = 1;

        A(2 * n - 2 + row - 1, 4 *(row - 1 - 1) + 1 + 4) = 3 * ( X(row)^2);
        A(2 * n - 2 + row - 1, 4 *(row - 1 - 1) + 2 + 4) = 2 * ( X(row));
        A(2 * n - 2 + row - 1, 4 *(row - 1 - 1) + 3 + 4) = 1;

    end 
    row = 2 * n - 2 + (n - 1) - 1;
    for ix = 2:n-1
        row = row + 1;
        A(row, 4 * (ix - 2) + 1) = 6 * X(ix);
        row = row + 1;
        A(row, 4 * (ix - 2) + 1) = 2;
        row = row + 1;

        A(row, 4 * (ix - 2) + 1 + 4) = 0 - 6 * X(ix);
        row = row + 1;
        A(row, 4 * (ix - 2) + 1 + 4) = 0 - 2;
    end


    %% SOLVE LSOE
    [sol, err] = function_solve_lsoe(A, B);

    %% PLOT - SHOW RESULTS

    for ix= 1:n-1
        %normalize
        maxRowFactor = max(abs(A(ix:end,ix:end)'))'
        A(ix:end,ix:end) =A(ix:end,ix:end)./maxRowFactor;
        B(ix:end) = B(ix:end) ./ maxRowFactor;

        %swap rows
        [~, pivotRow] = max(abs(A(ix:end,ix)));
        pivotRow = pivotRow + ix -1 ;
        if pivotRow ~= ix
            IP = eye(n);
            lIx = IP(ix,:);
            lPv = IP(pivotRow,:);

            IP(ix,:) = lPv;
            IP(pivotRow,:) = lIx;
            A = IP*A;
            B= IP*B;
        end

        %reduce
        M = eye(n);
        M(ix+1:end,ix) = -A(ix+1:end,ix)/A(ix,ix);
        A = M*A;
        B = M*B;
  
    end

    %back sub
    for ix = n:-1:1
        sol(ix) = (B(ix)-A(ix,ix+1:n)*sol(ix+1:n))/A(ix,ix);
    end

end

