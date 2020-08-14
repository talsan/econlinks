from foolcalls.athena_helpers import query

query_parameters = dict(return_df=False,
                        output_bucket='fool-calls-athena-output',
                        region='us-west-2', database='qcdb', work_group='primary',
                        sleep_between_requests=3, query_timeout=600,
                        cleanup=False)

s3_output_location = query(sql_string='SELECT '
                                      'idx.cid as cid,call_url,ticker,company_name,'
                                      'publication_time_published,publication_time_updated,period_end,'
                                      'fiscal_period_year,fiscal_period_qtr,call_date,duration_minutes,'
                                      'statement_num,section,statement_type,role,text'
                                      ' FROM fool_call_index idx '
                                      'JOIN fool_call_statements st '
                                      'ON idx.cid = st.cid',
                           **query_parameters)
