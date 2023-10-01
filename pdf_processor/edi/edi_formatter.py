import pandas as pd


def edi_211(
    df: pd.DataFrame,
    edi_key_col: str,
    edi_data_col: str,
) -> str:
    df['EDI_Segment'] = 'LIN*' + df[edi_key_col] + '*' + df[edi_data_col].astype(str) + '~'
    return df

def pandas_to_edi(
    edi_type: str,
    df: pd.DataFrame,
    edi_key_col: str,
    edi_data_col: str,
) -> str:
    f"""
    Convert Pandas data frame to edi format.
    """
    fns = {
        "211": edi_211,
    }
    # Make EDI segment from defined cols
    print(edi_type)
    df = fns[edi_type](
        df,
        edi_key_col,
        edi_data_col,
    )

    # Concatenate segments
    edi_data = '\n'.join(df['EDI_Segment'])
    return edi_data