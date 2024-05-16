def github() -> str:
    """
    Returns:
        str: github link
    """

    return "https://github.com/qiguangyan/481hw/blob/main/481hw6.py"
    
def std() -> str:
    """
    Returns a SQL query that calculates the std
    """
    query = """
    WITH bid_data AS (
        SELECT
            itemId,
            bidAmount,
            AVG(bidAmount) OVER (PARTITION BY itemId) AS mean_bid
        FROM bids
    ),
    bid_stats AS (
        SELECT
            itemId,
            COUNT(bidAmount) AS bid_count,
            SUM((bidAmount - mean_bid) * (bidAmount - mean_bid)) AS sum_squared_diffs
        FROM bid_data
        GROUP BY itemId
    )
    SELECT
        itemId,
        SQRT(sum_squared_diffs / (bid_count - 1)) AS std
    FROM bid_stats
    WHERE bid_count > 1;
    """
    return query

def bidder_spend_frac() -> str:
    """
    Returns a SQL query that calculates the total spend, total bids, and spend fraction
    """
    query = """
    WITH highest_bids AS (
        SELECT
            bidderName,
            itemId,
            MAX(bidAmount) AS highest_bid
        FROM bids
        GROUP BY bidderName, itemId
    ),
    total_spend AS (
        SELECT
            highBidderName AS bidderName,
            SUM(bidAmount) AS total_spend
        FROM bids
        WHERE highBidderName IS NOT NULL
        GROUP BY highBidderName
    ),
    total_bids AS (
        SELECT
            bidderName,
            SUM(highest_bid) AS total_bids
        FROM highest_bids
        GROUP BY bidderName
    )
    SELECT
        tb.bidderName,
        COALESCE(ts.total_spend, 0) AS total_spend,
        tb.total_bids,
        COALESCE(ts.total_spend, 0) / tb.total_bids AS spend_frac
    FROM total_bids tb
    LEFT JOIN total_spend ts ON tb.bidderName = ts.bidderName;
    """
    return query

def min_increment_freq() -> str:
    """
    Returns a SQL query that calculates the fraction of bids that are minimum bid increment
    above the previous high bid
    """
    query = """
    WITH valid_bids AS (
        SELECT
            b.itemId,
            b.bidAmount,
            i.bidIncrement,
            LAG(b.bidAmount) OVER (PARTITION BY b.itemId ORDER BY b.bidTime) AS prev_high_bid
        FROM bids b
        JOIN items i ON b.itemId = i.itemId
        WHERE i.isBuyNowUsed = 0
    ),
    increment_bids AS (
        SELECT
            COUNT(*) AS increment_count
        FROM valid_bids
        WHERE bidAmount = prev_high_bid + bidIncrement
    ),
    total_bids AS (
        SELECT
            COUNT(*) AS total_count
        FROM valid_bids
    )
    SELECT
        CAST(ib.increment_count AS FLOAT) / tb.total_count AS freq
    FROM increment_bids ib, total_bids tb;
    """
    return query

def win_perc_by_timestamp() -> str:
    """
    Returns a SQL query that calculates the winning percentage by timestamp
    """
    query = """
    WITH normalized_bids AS (
        SELECT
            b.bidLogId,
            b.itemId,
            b.bidTime,
            b.bidAmount,
            i.startTime,
            i.endTime,
            1.0 - (JULIANDAY(b.bidTime) - JULIANDAY(i.startTime)) / (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) AS norm_time,
            b.highBidderName,
            b.bidderName,
            CASE
                WHEN 1.0 - (JULIANDAY(b.bidTime) - JULIANDAY(i.startTime)) / 
                (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) BETWEEN 0 AND 0.1 THEN 1
                WHEN 1.0 - (JULIANDAY(b.bidTime) - JULIANDAY(i.startTime)) / 
                (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) BETWEEN 0.1 AND 0.2 THEN 2
                WHEN 1.0 - (JULIANDAY(b.bidTime) - JULIANDAY(i.startTime)) / 
                (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) BETWEEN 0.2 AND 0.3 THEN 3
                WHEN 1.0 - (JULIANDAY(b.bidTime) - JULIANDAY(i.startTime)) / 
                (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) BETWEEN 0.3 AND 0.4 THEN 4
                WHEN 1.0 - (JULIANDAY(b.bidTime) - JULIANDAY(i.startTime)) / 
                (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) BETWEEN 0.4 AND 0.5 THEN 5
                WHEN 1.0 - (JULIANDAY(b.bidTime) - JULIANDAY(i.startTime)) / 
                (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) BETWEEN 0.5 AND 0.6 THEN 6
                WHEN 1.0 - (JULIANDAY(b.bidTime) - JULIANDAY(i.startTime)) / 
                (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) BETWEEN 0.6 AND 0.7 THEN 7
                WHEN 1.0 - (JULIANDAY(b.bidTime) - JULIANDAY(i.startTime)) / 
                (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) BETWEEN 0.7 AND 0.8 THEN 8
                WHEN 1.0 - (JULIANDAY(b.bidTime) - JULIANDAY(i.startTime)) / 
                (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) BETWEEN 0.8 AND 0.9 THEN 9
                WHEN 1.0 - (JULIANDAY(b.bidTime) - JULIANDAY(i.startTime)) / 
                (JULIANDAY(i.endTime) - JULIANDAY(i.startTime)) BETWEEN 0.9 AND 1.0 THEN 10
            END AS timestamp_bin
        FROM bids b
        JOIN items i ON b.itemId = i.itemId
        WHERE JULIANDAY(i.endTime) - JULIANDAY(i.startTime) > 0
    ),
    win_count AS (
        SELECT
            timestamp_bin,
            COUNT(*) AS win_count
        FROM normalized_bids
        WHERE bidderName = highBidderName
        GROUP BY timestamp_bin
    ),
    total_count AS (
        SELECT
            timestamp_bin,
            COUNT(*) AS total_count
        FROM normalized_bids
        GROUP BY timestamp_bin
    )
    SELECT
        tc.timestamp_bin,
        COALESCE(wc.win_count, 0) * 1.0 / tc.total_count AS win_perc
    FROM total_count tc
    LEFT JOIN win_count wc ON tc.timestamp_bin = wc.timestamp_bin
    ORDER BY tc.timestamp_bin;
    """
    return query