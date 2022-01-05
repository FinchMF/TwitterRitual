import torch
import torch.nn as nn


def forward_back_prop(
    model: object,
    optimizer: object,
    loss_func: object,
    x: list,
    y: list,
    hidden: list,
    train_on_gpu: bool =torch.cuda.is_available()
) -> tuple:

    if train_on_gpu:
        x, y = x.cuda(), y.cuda()

    hidden = tuple([each.data for each in hidden])

    model.zero_grad()
    ouput, hidden = model(x, hidden)

    loss = loss_func(output, y)
    loss.backward()

    clip = 5
    nn.utils.clip_grad_norm_(model.parameters(), clip)
    optimizer.step()

    return loss.item(), hidden


def run_training_procedure(
    model: object,
    batch_size: int,
    optimizer: object,
    loss_func: object,
    n_epochs: int,
    training_data: object,
    show_every_n_batches: int =100
) -> object:

    batch_losses: list = []

    model.train()

    print(f' | Training for {n_epochs} epoch(s).....')
    for e in range(1, n_epochs + 1):

        hidden = model.init_hidden(batch_size)

        for batch_idx, (inputs, labels) in enumerate(training_data, 1):

            n_batches: int = len(training_data.dataset) // batch_size

            if batch_idx > n_batches:
                break

            loss, hidden = forward_back_prop(
                            model=model,
                            optimizer=optimizer,
                            loss_func=loss_func,
                            x=inputs,
                            y=labels,
                            hidden=hidden
            )
            batch_losses.append(loss)

            if batch_idx % show_every_n_batches == 0:
                print(f' | EPOCH: {e:>4}/{n_epochs:>4} -- LOSS: {np.average(batch_losses)}')
                batch_losses: list = []

    return model

