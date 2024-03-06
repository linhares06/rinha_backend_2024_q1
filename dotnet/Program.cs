using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;

using ClientApi;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(opt => 
    opt.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

var app = builder.Build();

app.MapGet("/clientes", async (AppDbContext db) =>
    await db.Client.ToListAsync());

app.MapPost("/clientes/{id}/transacoes", async (int id, Transaction transaction, AppDbContext db) =>
{
    try 
    {
        Validator.ValidateObject(transaction, new ValidationContext(transaction), validateAllProperties: true);

        var client = await db.Client.FindAsync(id);

        if (client is null) return Results.NotFound("Id indexistente.");

        int saldo = 0;

        if (transaction.Tipo == 'd')
        {
            saldo = client.Saldo - transaction.Valor;
            if (saldo + client.Limite < 0) return Results.UnprocessableEntity("Ta querendo gastar mais do que tem, champz");
        } 
        else 
        {
            saldo = client.Saldo + transaction.Valor;
        }

        client.Saldo = saldo;
        transaction.ClientId = id;

        db.Transaction.Add(transaction);
        await db.SaveChangesAsync();

        var result = new { limite = client.Limite, saldo = client.Saldo };

        return Results.Ok(result);
    }
    catch (Exception ex)
    {
        return Results.UnprocessableEntity(ex.Message);
    }  
});

app.MapGet("/clientes/{id}/extrato", async (int id, AppDbContext db) =>
{
    try
    {
        var client = await db.Client.FindAsync(id);

        if (client is null) return Results.NotFound("Id indexistente.");

        var transactions = await db.Transaction
        .Where(t => t.ClientId  == id)
        .OrderByDescending(t => t.RealizadaEm)
        .Take(10)
        .Select(t => new {
            t.Valor,
            t.Tipo,
            t.Descricao,
            t.RealizadaEm
        })
        .ToListAsync();

        var result = new {
            saldo = new {
                total = client.Saldo,
                data_extrato = DateTime.Now,
                client.Limite,
            },
            ultimas_transacoes = transactions
        };

        return Results.Ok(result);
    }
    catch(Exception ex)
    {
        return Results.UnprocessableEntity(ex.Message);
    }
});

app.Run();