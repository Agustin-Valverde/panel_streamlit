import polars as pl
import requests
import msgspec
from datetime import date, datetime, timedelta

def create_ratio(ratio_col: str) -> pl.Expr:
    return (
        pl.when(pl.col(ratio_col) < 0.2).then(pl.lit("A"))
        .when(pl.col(ratio_col) < 0.4).then(pl.lit("B"))
        .when(pl.col(ratio_col) < 0.6).then(pl.lit("C"))
        .when(pl.col(ratio_col) < 0.8).then(pl.lit("D"))
        .otherwise(pl.lit("E")).alias("ratio")
    )

def create_shippter_df():
    main_date = date.today() - timedelta(days=30)

    SECRET = "shippter2021"
    url = "https://us-west-2.aws.data.mongodb-api.com/app/application-0-yrtca/endpoint/"
    url += f"quotes/details?secret={SECRET}&from={main_date}"

    print("Iniciado lectura de datos...")
    
    r = requests.get(url)
    print(r.status_code)

    response_dict = msgspec.json.decode(r.content)["quotes"]

    rod = (
        pl.LazyFrame(response_dict, strict=False)
        .filter(pl.col("isSaas") == False)
        .select(pl.col("createdAt", "roi", "client", "type", "incoterm", "origin", "salesRepresentative",
                       "services", "clientCurrentRatio", "transport", "shippingAgency", "discount", "etd", "eta"))
        .unnest("services")
        .with_columns(
            pl.all_horizontal(pl.col("freight", "localTransport", "customs", "insurance").alias("all_services")),
            pl.when(pl.col("transport") == "AIR").then(pl.lit("AIR")).otherwise(pl.col("type")).alias("type"),
            pl.when(pl.col("incoterm").is_in(["CIF", "COURIER", "CFR"])).then(pl.lit("CIF")).otherwise(pl.col("incoterm")).alias("incoterm"),
            pl.col("createdAt", "etd", "eta").str.to_datetime().dt.date(),
            create_ratio("clientCurrentRatio")
        )
    )

    rod_saas = (
        pl.LazyFrame(response_dict, strict=False)
        .filter(pl.col("isSaas") == True)
    )

    rod.write_csv("rod.csv")

    return rod


def read_rod_csv():
    df = pl.read_csv("data\\rod.csv")
    return df


if __name__=="__main__":
    rod = create_shippter_df()
    rod.glimpse()
